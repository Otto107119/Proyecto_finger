from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user

from app import db
from app.models import (
    Paciente,
    ActividadSocial,
    ActividadSocialEconomia,
    ActividadSocialPadreMadre,
    ActividadSocialHermano,
    ActividadSocialHijo
)
from app.forms.actividad_social import ActividadSocialForm, HermanoForm, HijoForm


actividad_social_bp = Blueprint(
    "actividad_social",
    __name__,
    url_prefix="/pacientes/<int:paciente_id>/actividad_social"
)


@actividad_social_bp.route("", methods=["GET"])
@login_required
def actividad_social_lista(paciente_id):
    paciente = Paciente.query.get_or_404(paciente_id)

    actividades = ActividadSocial.query.filter_by(
        paciente_id=paciente.id
    ).order_by(ActividadSocial.created_at.desc()).all()

    return render_template(
        "actividad_social/actividad_social_lista.html",
        paciente=paciente,
        actividades=actividades
    )


@actividad_social_bp.route("/nueva", methods=["POST"])
@login_required
def actividad_social_nueva(paciente_id):
    paciente = Paciente.query.get_or_404(paciente_id)

    nueva = ActividadSocial(
        paciente_id=paciente.id,
        finalizado=False
    )
    db.session.add(nueva)
    db.session.commit()

    flash("Nueva captura de actividad social creada correctamente.", "success")
    return redirect(url_for(
        "actividad_social.actividad_social_detalle",
        paciente_id=paciente.id,
        actividad_id=nueva.id
    ))


@actividad_social_bp.route("/<int:actividad_id>", methods=["GET", "POST"])
@login_required
def actividad_social_detalle(paciente_id, actividad_id):
    paciente = Paciente.query.get_or_404(paciente_id)

    actividad = ActividadSocial.query.filter_by(
        id=actividad_id,
        paciente_id=paciente.id
    ).first_or_404()

    seccion = request.args.get("seccion", "datos_generales")

    editable_social = (
        current_user.rol == "admin"
        or (
            current_user.rol == "capturista"
            and not actividad.finalizado
        )
    )

    padre = ActividadSocialPadreMadre.query.filter_by(
        actividad_social_id=actividad.id,
        tipo="padre"
    ).first()

    madre = ActividadSocialPadreMadre.query.filter_by(
        actividad_social_id=actividad.id,
        tipo="madre"
    ).first()

    hermanos = ActividadSocialHermano.query.filter_by(
        actividad_social_id=actividad.id
    ).all()

    hijos = ActividadSocialHijo.query.filter_by(
        actividad_social_id=actividad.id
    ).all()

    form = ActividadSocialForm()
    hermano_form = HermanoForm()
    hijo_form = HijoForm()

    # Precargar SOLO en GET
    if request.method == "GET":
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

    # Guardar hermanos
    if editable_social and seccion == "hermanos" and hermano_form.validate_on_submit():
        nuevo = ActividadSocialHermano(
            actividad_social_id=actividad.id,
            nombre=hermano_form.nombre.data,
            edad=hermano_form.edad.data,
            relacion=hermano_form.relacion.data,
            donde_vive=hermano_form.donde_vive.data,
            enfermedad=hermano_form.enfermedad.data
        )
        db.session.add(nuevo)
        db.session.commit()

        flash("Hermano agregado correctamente.", "success")
        return redirect(url_for(
            "actividad_social.actividad_social_detalle",
            paciente_id=paciente.id,
            actividad_id=actividad.id,
            seccion="hermanos"
        ))

    # Guardar hijos
    if editable_social and seccion == "hijos" and hijo_form.validate_on_submit():
        nuevo = ActividadSocialHijo(
            actividad_social_id=actividad.id,
            nombre=hijo_form.nombre.data,
            edad=hijo_form.edad.data,
            estado_civil=hijo_form.estado_civil.data,
            relacion=hijo_form.relacion.data,
            donde_vive=hijo_form.donde_vive.data,
            enfermedad=hijo_form.enfermedad.data,
            numero_hijos=hijo_form.numero_hijos.data
        )
        db.session.add(nuevo)
        db.session.commit()

        flash("Hijo agregado correctamente.", "success")
        return redirect(url_for(
            "actividad_social.actividad_social_detalle",
            paciente_id=paciente.id,
            actividad_id=actividad.id,
            seccion="hijos"
        ))

    # Guardar SOLO la sección actual
    if editable_social and seccion in ["datos_generales", "economia", "padres"] and form.validate_on_submit():

        # =========================
        # DATOS GENERALES
        # =========================
        if seccion == "datos_generales":
            actividad.seguridad_social = form.seguridad_social.data
            actividad.tiempo_residencia_ameca = form.tiempo_residencia_ameca.data
            actividad.tipo_vivienda = form.tipo_vivienda.data
            actividad.migracion = form.migracion.data
            actividad.observaciones = form.observaciones.data

        # =========================
        # ECONOMÍA
        # =========================
        elif seccion == "economia":
            if not actividad.economia:
                actividad.economia = ActividadSocialEconomia(
                    actividad_social_id=actividad.id
                )
                db.session.add(actividad.economia)

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

        # =========================
        # PADRES
        # =========================
        elif seccion == "padres":
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

        flash("Información guardada correctamente.", "success")

        accion = request.form.get("accion")
        if accion == "siguiente":
            siguiente = {
                "datos_generales": "economia",
                "economia": "padres",
                "padres": "hermanos"
            }.get(seccion, seccion)

            return redirect(url_for(
                "actividad_social.actividad_social_detalle",
                paciente_id=paciente.id,
                actividad_id=actividad.id,
                seccion=siguiente
            ))

        return redirect(url_for(
            "actividad_social.actividad_social_detalle",
            paciente_id=paciente.id,
            actividad_id=actividad.id,
            seccion=seccion
        ))

    return render_template(
        "actividad_social/actividad_social_detalle.html",
        paciente=paciente,
        actividad=actividad,
        form=form,
        hermano_form=hermano_form,
        hijo_form=hijo_form,
        hermanos=hermanos,
        hijos=hijos,
        padre=padre,
        madre=madre,
        seccion=seccion,
        editable_social=editable_social
    )


@actividad_social_bp.route("/<int:actividad_id>/hermano/<int:hermano_id>/eliminar", methods=["POST"])
@login_required
def actividad_social_hermano_eliminar(paciente_id, actividad_id, hermano_id):
    hermano = ActividadSocialHermano.query.get_or_404(hermano_id)
    actividad = ActividadSocial.query.filter_by(
        id=actividad_id,
        paciente_id=paciente_id
    ).first_or_404()

    if current_user.rol not in ["admin", "capturista"] or actividad.finalizado:
        flash("No tienes permiso para eliminar hermanos.", "danger")
        return redirect(url_for(
            "actividad_social.actividad_social_detalle",
            paciente_id=paciente_id,
            actividad_id=actividad_id,
            seccion="hermanos"
        ))

    db.session.delete(hermano)
    db.session.commit()

    flash("Hermano eliminado correctamente.", "success")
    return redirect(url_for(
        "actividad_social.actividad_social_detalle",
        paciente_id=paciente_id,
        actividad_id=actividad_id,
        seccion="hermanos"
    ))


@actividad_social_bp.route("/<int:actividad_id>/hijo/<int:hijo_id>/eliminar", methods=["POST"])
@login_required
def actividad_social_hijo_eliminar(paciente_id, actividad_id, hijo_id):
    hijo = ActividadSocialHijo.query.get_or_404(hijo_id)
    actividad = ActividadSocial.query.filter_by(
        id=actividad_id,
        paciente_id=paciente_id
    ).first_or_404()

    if current_user.rol not in ["admin", "capturista"] or actividad.finalizado:
        flash("No tienes permiso para eliminar hijos.", "danger")
        return redirect(url_for(
            "actividad_social.actividad_social_detalle",
            paciente_id=paciente_id,
            actividad_id=actividad_id,
            seccion="hijos"
        ))

    db.session.delete(hijo)
    db.session.commit()

    flash("Hijo eliminado correctamente.", "success")
    return redirect(url_for(
        "actividad_social.actividad_social_detalle",
        paciente_id=paciente_id,
        actividad_id=actividad_id,
        seccion="hijos"
    ))


@actividad_social_bp.route("/<int:actividad_id>/finalizar", methods=["POST"])
@login_required
def actividad_social_finalizar(paciente_id, actividad_id):
    actividad = ActividadSocial.query.filter_by(
        id=actividad_id,
        paciente_id=paciente_id
    ).first_or_404()

    if current_user.rol not in ["admin", "capturista"]:
        flash("No tienes permiso para finalizar esta captura.", "danger")
        return redirect(url_for(
            "actividad_social.actividad_social_detalle",
            paciente_id=paciente_id,
            actividad_id=actividad_id,
            seccion="resumen"
        ))

    actividad.finalizado = True
    db.session.commit()

    flash("Actividad social finalizada correctamente.", "success")
    return redirect(url_for(
        "actividad_social.actividad_social_lista",
        paciente_id=paciente_id
    ))