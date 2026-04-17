from flask import Blueprint, render_template, redirect, url_for, flash, request
from app import db
from app.models import (
    Usuario, Paciente, ActividadFisica,
    ActividadSocial, ActividadSocialEconomia,
    ActividadSocialPadreMadre, ActividadSocialHermano, ActividadSocialHijo,
    HistorialClinico
)
from app.forms import (
    RegistroForm, LoginForm, PacienteForm, ActividadFisicaForm,
    ActividadSocialForm, HermanoForm, HijoForm,
    HistorialClinicoForm
)
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask import abort
from functools import wraps
from datetime import datetime

from app.permisos import puede_editar_area


def role_required(*roles):
    def decorator(func):
        @wraps(func)
        @login_required
        def wrapper(*args, **kwargs):
            if current_user.rol not in roles:
                abort(403)
            return func(*args, **kwargs)
        return wrapper
    return decorator


main = Blueprint('main', __name__)

@main.route("/")
@login_required
def index():
    return render_template("dashboard.html")

@main.route("/registro", methods=["GET", "POST"])
def registro():
    form = RegistroForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        nuevo_usuario = Usuario(
            nombre=form.nombre.data,
            correo=form.correo.data,
            password=hashed_password,
            rol="capturista"
            )
        db.session.add(nuevo_usuario)
        db.session.commit()
        flash("Usuario registrado correctamente")
        return redirect(url_for("main.login"))
    return render_template("auth/registro.html", form=form)

@main.route("/crear_usuario", methods=["GET", "POST"])
@role_required("admin")
def crear_usuario():
    form = RegistroForm()

    if form.validate_on_submit():
        from flask import request

        rol = request.form.get("rol")

        hashed_password = generate_password_hash(form.password.data)

        nuevo_usuario = Usuario(
            nombre=form.nombre.data,
            correo=form.correo.data,
            password=hashed_password,
            rol=rol
        )

        db.session.add(nuevo_usuario)
        db.session.commit()
        flash("Usuario creado por administrador")
        return redirect(url_for("main.index"))

    return render_template("auth/crear_usuario.html", form=form)

@main.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(correo=form.correo.data).first()
        if usuario and check_password_hash(usuario.password, form.password.data):
            login_user(usuario)
            return redirect(url_for("main.index"))
        flash("Credenciales incorrectas")
    return render_template("auth/login.html", form=form)

@main.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.login"))



@main.route("/pacientes")
@login_required
def pacientes_lista():
    pacientes = Paciente.query.order_by(Paciente.nombre.asc()).all()
    return render_template("pacientes/pacientes_lista.html", pacientes=pacientes)

@main.route("/pacientes/nuevo", methods=["GET", "POST"])
@login_required
def pacientes_nuevo():
    form = PacienteForm()

    if form.validate_on_submit():
        nuevo = Paciente(
            nombre=form.nombre.data,
            fecha_nacimiento=form.fecha_nacimiento.data,
            genero=form.genero.data,
            usuario_id=current_user.id
        )
        db.session.add(nuevo)
        db.session.commit()
        
        flash("Paciente registrado correctamente ✅")
        return redirect(url_for("main.pacientes_lista"))

    return render_template("pacientes/pacientes_nuevo.html", form=form)

@main.route("/pacientes/<int:paciente_id>")
@login_required
def pacientes_detalle(paciente_id):
    paciente = Paciente.query.get_or_404(paciente_id)
    return render_template("pacientes/pacientes_detalle.html", paciente=paciente)




@main.route("/pacientes/<int:paciente_id>/actividad_fisica")
@login_required
def actividad_fisica_lista(paciente_id):
    paciente = Paciente.query.get_or_404(paciente_id)
    actividades = ActividadFisica.query.filter_by(paciente_id=paciente_id).order_by(ActividadFisica.fecha.desc()).all()
    return render_template("actividad_fisica/actividad_fisica_lista.html", paciente=paciente, actividades=actividades)


@main.route("/pacientes/<int:paciente_id>/actividad_fisica/nueva", methods=["GET", "POST"])
@role_required("admin", "capturista")
def actividad_fisica_nueva(paciente_id):
    paciente = Paciente.query.get_or_404(paciente_id)
    form = ActividadFisicaForm()

    if form.validate_on_submit():
        nueva = ActividadFisica(
            tipo=form.tipo.data,
            duracion_min=form.duracion_min.data,
            observaciones=form.observaciones.data,
            paciente_id=paciente.id,
            usuario_id=current_user.id
        )
        db.session.add(nueva)
        db.session.commit()
        flash("Actividad física registrada ✅")
        return redirect(url_for("main.actividad_fisica_lista", paciente_id=paciente.id))

    return render_template("actividad_fisica/actividad_fisica_nueva.html", paciente=paciente, form=form)


@main.route("/actividad_fisica/<int:actividad_id>/editar", methods=["GET", "POST"])
@role_required("admin", "capturista")
def actividad_fisica_editar(actividad_id):
    actividad = ActividadFisica.query.get_or_404(actividad_id)

    # (opcional) si quieres que capturista SOLO edite lo suyo:
    if current_user.rol == "capturista" and actividad.usuario_id != current_user.id:
        abort(403)

    form = ActividadFisicaForm(obj=actividad)

    if form.validate_on_submit():
        actividad.tipo = form.tipo.data
        actividad.duracion_min = form.duracion_min.data
        actividad.observaciones = form.observaciones.data
        db.session.commit()
        flash("Actividad actualizada ✅")
        return redirect(url_for("main.actividad_fisica_lista", paciente_id=actividad.paciente_id))

    return render_template("actividad_fisica/actividad_fisica_editar.html", form=form, actividad=actividad)


@main.route("/actividad_fisica/<int:actividad_id>/eliminar", methods=["POST"])
@role_required("admin")
def actividad_fisica_eliminar(actividad_id):
    actividad = ActividadFisica.query.get_or_404(actividad_id)
    paciente_id = actividad.paciente_id
    db.session.delete(actividad)
    db.session.commit()
    flash("Actividad eliminada 🗑️")
    return redirect(url_for("main.actividad_fisica_lista", paciente_id=paciente_id))



@main.route("/pacientes/<int:paciente_id>/actividad_social", methods=["GET", "POST"])
@login_required
def actividad_social_detalle(paciente_id):
    paciente = Paciente.query.get_or_404(paciente_id)
    editable_social = puede_editar_area(current_user, "actividad_social")

    actividad = ActividadSocial.query.filter_by(paciente_id=paciente.id).first()

    # =====================================================
    # SOLO crear registros automáticamente si puede editar
    # =====================================================
    if not actividad and editable_social:
        actividad = ActividadSocial(paciente_id=paciente.id)
        db.session.add(actividad)
        db.session.flush()

        economia = ActividadSocialEconomia(actividad_social_id=actividad.id)
        db.session.add(economia)
        db.session.commit()

    if actividad and not actividad.economia and editable_social:
        economia = ActividadSocialEconomia(actividad_social_id=actividad.id)
        db.session.add(economia)
        db.session.commit()

    seccion = request.args.get("seccion", "datos_generales")

    form = ActividadSocialForm()
    hermano_form = HermanoForm()
    hijo_form = HijoForm()

    hermanos = []
    hijos = []
    padre = None
    madre = None

    if actividad:
        hermanos = ActividadSocialHermano.query.filter_by(
            actividad_social_id=actividad.id
        ).order_by(ActividadSocialHermano.id.asc()).all()

        hijos = ActividadSocialHijo.query.filter_by(
            actividad_social_id=actividad.id
        ).order_by(ActividadSocialHijo.id.asc()).all()

        padre = ActividadSocialPadreMadre.query.filter_by(
            actividad_social_id=actividad.id,
            tipo="padre"
        ).first()

        madre = ActividadSocialPadreMadre.query.filter_by(
            actividad_social_id=actividad.id,
            tipo="madre"
        ).first()

    # =====================================================
    # BLOQUEO GENERAL DE POST SI NO TIENE PERMISOS
    # =====================================================
    if request.method == "POST" and not editable_social:
        flash("No tienes permisos para modificar Actividad Social.", "danger")
        return redirect(url_for(
            "main.actividad_social_detalle",
            paciente_id=paciente.id,
            seccion=seccion
        ))

    # =====================================================
    # GUARDAR HERMANO
    # =====================================================
    if editable_social and actividad and seccion == "hermanos" and hermano_form.validate_on_submit():
        nuevo_hermano = ActividadSocialHermano(
            actividad_social_id=actividad.id,
            nombre=hermano_form.nombre.data,
            edad=hermano_form.edad.data,
            relacion=hermano_form.relacion.data,
            donde_vive=hermano_form.donde_vive.data,
            enfermedad=hermano_form.enfermedad.data
        )
        db.session.add(nuevo_hermano)
        db.session.commit()
        flash("Hermano agregado correctamente ✅", "success")
        return redirect(url_for(
            "main.actividad_social_detalle",
            paciente_id=paciente.id,
            seccion="hermanos"
        ))

    # =====================================================
    # GUARDAR HIJO
    # =====================================================
    if editable_social and actividad and seccion == "hijos" and hijo_form.validate_on_submit():
        nuevo_hijo = ActividadSocialHijo(
            actividad_social_id=actividad.id,
            nombre=hijo_form.nombre.data,
            edad=hijo_form.edad.data,
            estado_civil=hijo_form.estado_civil.data,
            relacion=hijo_form.relacion.data,
            donde_vive=hijo_form.donde_vive.data,
            enfermedad=hijo_form.enfermedad.data,
            numero_hijos=hijo_form.numero_hijos.data
        )
        db.session.add(nuevo_hijo)
        db.session.commit()
        flash("Hijo agregado correctamente ✅", "success")
        return redirect(url_for(
            "main.actividad_social_detalle",
            paciente_id=paciente.id,
            seccion="hijos"
        ))

    # =====================================================
    # GUARDAR FORMULARIO PRINCIPAL
    # =====================================================
    if editable_social and actividad and seccion in ["datos_generales", "economia", "padres"] and form.validate_on_submit():
        actividad.seguridad_social = form.seguridad_social.data
        actividad.tiempo_residencia_ameca = form.tiempo_residencia_ameca.data
        actividad.tipo_vivienda = form.tipo_vivienda.data
        actividad.migracion = form.migracion.data
        actividad.observaciones = form.observaciones.data

        if not actividad.economia:
            actividad.economia = ActividadSocialEconomia()

        actividad.economia.ingreso_entrevistado = form.ingreso_entrevistado.data or 0
        actividad.economia.otros_ingresos = form.otros_ingresos.data or 0
        actividad.economia.renta = form.renta.data or 0
        actividad.economia.colegiaturas = form.colegiaturas.data or 0
        actividad.economia.alimentacion = form.alimentacion.data or 0
        actividad.economia.gastos_medicos = form.gastos_medicos.data or 0
        actividad.economia.transporte = form.transporte.data or 0
        actividad.economia.diversion = form.diversion.data or 0
        actividad.economia.gasolina = form.gasolina.data or 0
        actividad.economia.pagos_tarjetas = form.pagos_tarjetas.data or 0
        actividad.economia.luz = form.luz.data or 0
        actividad.economia.ahorro = form.ahorro.data or 0
        actividad.economia.agua = form.agua.data or 0
        actividad.economia.deudas = form.deudas.data or 0
        actividad.economia.gas = form.gas.data or 0
        actividad.economia.ropa = form.ropa.data or 0
        actividad.economia.telefono = form.telefono.data or 0
        actividad.economia.calzado = form.calzado.data or 0
        actividad.economia.telefono_celular = form.telefono_celular.data or 0
        actividad.economia.alcohol_cigarros = form.alcohol_cigarros.data or 0
        actividad.economia.cable = form.cable.data or 0
        actividad.economia.internet = form.internet.data or 0
        actividad.economia.otros_gastos = form.otros_gastos.data or 0
        actividad.economia.empleados_domesticos = form.empleados_domesticos.data or 0

        actividad.economia.calcular_totales()

        if not padre:
            padre = ActividadSocialPadreMadre(
                actividad_social_id=actividad.id,
                tipo="padre"
            )
            db.session.add(padre)

        padre.nombre = form.padre_nombre.data
        padre.edad_o_tiempo_vida = form.padre_edad_o_tiempo_vida.data
        padre.vive = form.padre_vive.data
        padre.causa_muerte = form.padre_causa_muerte.data
        padre.enfermedad = form.padre_enfermedad.data

        if not madre:
            madre = ActividadSocialPadreMadre(
                actividad_social_id=actividad.id,
                tipo="madre"
            )
            db.session.add(madre)

        madre.nombre = form.madre_nombre.data
        madre.edad_o_tiempo_vida = form.madre_edad_o_tiempo_vida.data
        madre.vive = form.madre_vive.data
        madre.causa_muerte = form.madre_causa_muerte.data
        madre.enfermedad = form.madre_enfermedad.data

        db.session.commit()
        flash("Actividad social actualizada correctamente ✅", "success")

        accion = request.form.get("accion", "guardar")

        if accion == "siguiente":
            if seccion == "datos_generales":
                return redirect(url_for("main.actividad_social_detalle", paciente_id=paciente.id, seccion="economia"))
            elif seccion == "economia":
                return redirect(url_for("main.actividad_social_detalle", paciente_id=paciente.id, seccion="padres"))
            elif seccion == "padres":
                return redirect(url_for("main.actividad_social_detalle", paciente_id=paciente.id, seccion="hermanos"))
            elif seccion == "hermanos":
                return redirect(url_for("main.actividad_social_detalle", paciente_id=paciente.id, seccion="hijos"))
            elif seccion == "hijos":
                return redirect(url_for("main.actividad_social_detalle", paciente_id=paciente.id, seccion="resumen"))

        elif accion == "anterior":
            if seccion == "economia":
                return redirect(url_for("main.actividad_social_detalle", paciente_id=paciente.id, seccion="datos_generales"))
            elif seccion == "padres":
                return redirect(url_for("main.actividad_social_detalle", paciente_id=paciente.id, seccion="economia"))
            elif seccion == "hermanos":
                return redirect(url_for("main.actividad_social_detalle", paciente_id=paciente.id, seccion="padres"))
            elif seccion == "hijos":
                return redirect(url_for("main.actividad_social_detalle", paciente_id=paciente.id, seccion="hermanos"))
            elif seccion == "resumen":
                return redirect(url_for("main.actividad_social_detalle", paciente_id=paciente.id, seccion="hijos"))

        return redirect(url_for(
            "main.actividad_social_detalle",
            paciente_id=paciente.id,
            seccion=seccion
        ))

    # =====================================================
    # PRECARGA DE DATOS
    # =====================================================
    if request.method == "GET" and actividad:
        form.seguridad_social.data = actividad.seguridad_social
        form.tiempo_residencia_ameca.data = actividad.tiempo_residencia_ameca
        form.tipo_vivienda.data = actividad.tipo_vivienda
        form.migracion.data = actividad.migracion
        form.observaciones.data = actividad.observaciones

        if actividad.economia:
            form.ingreso_entrevistado.data = actividad.economia.ingreso_entrevistado
            form.otros_ingresos.data = actividad.economia.otros_ingresos
            form.renta.data = actividad.economia.renta
            form.colegiaturas.data = actividad.economia.colegiaturas
            form.alimentacion.data = actividad.economia.alimentacion
            form.gastos_medicos.data = actividad.economia.gastos_medicos
            form.transporte.data = actividad.economia.transporte
            form.diversion.data = actividad.economia.diversion
            form.gasolina.data = actividad.economia.gasolina
            form.pagos_tarjetas.data = actividad.economia.pagos_tarjetas
            form.luz.data = actividad.economia.luz
            form.ahorro.data = actividad.economia.ahorro
            form.agua.data = actividad.economia.agua
            form.deudas.data = actividad.economia.deudas
            form.gas.data = actividad.economia.gas
            form.ropa.data = actividad.economia.ropa
            form.telefono.data = actividad.economia.telefono
            form.calzado.data = actividad.economia.calzado
            form.telefono_celular.data = actividad.economia.telefono_celular
            form.alcohol_cigarros.data = actividad.economia.alcohol_cigarros
            form.cable.data = actividad.economia.cable
            form.internet.data = actividad.economia.internet
            form.otros_gastos.data = actividad.economia.otros_gastos
            form.empleados_domesticos.data = actividad.economia.empleados_domesticos

        if padre:
            form.padre_nombre.data = padre.nombre
            form.padre_edad_o_tiempo_vida.data = padre.edad_o_tiempo_vida
            form.padre_vive.data = padre.vive
            form.padre_causa_muerte.data = padre.causa_muerte
            form.padre_enfermedad.data = padre.enfermedad

        if madre:
            form.madre_nombre.data = madre.nombre
            form.madre_edad_o_tiempo_vida.data = madre.edad_o_tiempo_vida
            form.madre_vive.data = madre.vive
            form.madre_causa_muerte.data = madre.causa_muerte
            form.madre_enfermedad.data = madre.enfermedad

    return render_template(
        "actividad_social/actividad_social_detalle.html",
        paciente=paciente,
        actividad=actividad,
        form=form,
        hermano_form=hermano_form,
        hermanos=hermanos,
        hijo_form=hijo_form,
        hijos=hijos,
        seccion=seccion,
        editable_social=editable_social
    )


@main.route("/actividad_social/hermano/<int:hermano_id>/eliminar", methods=["POST"])
@login_required
def actividad_social_hermano_eliminar(hermano_id):
    hermano = ActividadSocialHermano.query.get_or_404(hermano_id)
    actividad = ActividadSocial.query.get_or_404(hermano.actividad_social_id)
    paciente_id = actividad.paciente_id

    if not puede_editar_area(current_user, "actividad_social"):
        flash("No tienes permisos para eliminar hermanos en Actividad Social.", "danger")
        return redirect(url_for("main.actividad_social_detalle", paciente_id=paciente_id, seccion="hermanos"))

    db.session.delete(hermano)
    db.session.commit()

    flash("Hermano eliminado correctamente 🗑️", "success")
    return redirect(url_for("main.actividad_social_detalle", paciente_id=paciente_id, seccion="hermanos"))

@main.route("/actividad_social/hijo/<int:hijo_id>/eliminar", methods=["POST"])
@login_required
def actividad_social_hijo_eliminar(hijo_id):
    hijo = ActividadSocialHijo.query.get_or_404(hijo_id)
    actividad = ActividadSocial.query.get_or_404(hijo.actividad_social_id)
    paciente_id = actividad.paciente_id

    if not puede_editar_area(current_user, "actividad_social"):
        flash("No tienes permisos para eliminar hijos en Actividad Social.", "danger")
        return redirect(url_for("main.actividad_social_detalle", paciente_id=paciente_id, seccion="hijos"))

    db.session.delete(hijo)
    db.session.commit()

    flash("Hijo eliminado correctamente 🗑️", "success")
    return redirect(url_for("main.actividad_social_detalle", paciente_id=paciente_id, seccion="hijos"))

@main.route("/actividad_social/<int:actividad_id>/finalizar", methods=["POST"])
@login_required
def actividad_social_finalizar(actividad_id):
    actividad = ActividadSocial.query.get_or_404(actividad_id)

    if not puede_editar_area(current_user, "actividad_social"):
        flash("No tienes permisos para finalizar Actividad Social.", "danger")
        return redirect(url_for(
            "main.actividad_social_detalle",
            paciente_id=actividad.paciente_id,
            seccion="resumen"
        ))

    actividad.finalizado = True
    db.session.commit()

    flash("Actividad Social finalizada correctamente ✅", "success")
    return redirect(url_for(
        "main.actividad_social_detalle",
        paciente_id=actividad.paciente_id,
        seccion="resumen"
    ))



@main.route("/pacientes/<int:paciente_id>/historial-clinico/datos-generales", methods=["GET", "POST"])
@login_required
def historial_clinico_datos_generales(paciente_id):
    paciente = Paciente.query.get_or_404(paciente_id)

    historial = HistorialClinico.query.filter_by(paciente_id=paciente.id).first()
    if not historial:
        historial = HistorialClinico(paciente_id=paciente.id)
        db.session.add(historial)
        db.session.commit()

    form = HistorialClinicoForm(obj=historial)

    if form.validate_on_submit():
        form.populate_obj(historial)
        db.session.commit()
        flash("Datos generales guardados correctamente.", "success")
        return redirect(url_for("main.historial_clinico_area_social", paciente_id=paciente.id))

    return render_template(
        "historial_clinico/datos_generales.html",
        paciente=paciente,
        historial=historial,
        form=form
    )


@main.route("/pacientes/<int:paciente_id>/historial-clinico/area-social", methods=["GET", "POST"])
@login_required
def historial_clinico_area_social(paciente_id):
    paciente = Paciente.query.get_or_404(paciente_id)

    historial = HistorialClinico.query.filter_by(paciente_id=paciente.id).first()
    if not historial:
        historial = HistorialClinico(paciente_id=paciente.id)
        db.session.add(historial)
        db.session.commit()

    form = HistorialClinicoForm(obj=historial)

    if form.validate_on_submit():
        form.populate_obj(historial)
        db.session.commit()
        flash("Área social guardada correctamente.", "success")
        return redirect(url_for("main.historial_clinico_area_social", paciente_id=paciente.id))

    return render_template(
        "historial_clinico/area_social.html",
        paciente=paciente,
        historial=historial,
        form=form
    )