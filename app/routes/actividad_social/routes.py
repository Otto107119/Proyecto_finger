from datetime import datetime
from app import db
from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user

from app.models import (
    Paciente,
    ActividadSocial,
    ActividadSocialEconomia,
    ActividadSocialPadreMadre,
    ActividadSocialHermano,
    ActividadSocialHijo,
    ActividadSocialSaludMental,
    ActividadSocialGDS15,
    ActividadSocialKatz,
    ActividadSocialLawtonBrody,
)

from app.forms.actividad_social import (
    ActividadSocialForm,
    HermanoForm,
    HijoForm,
    ActividadSocialSaludMentalForm,
    ActividadSocialGDS15Form,
    ActividadSocialKatzForm,
    ActividadSocialLawtonBrodyForm,
)

from app.routes.actividad_social.salud_mental_utils import (
    interpretar_gds,
    calcular_katz_total,
    interpretar_katz
)

from app.routes.actividad_social.escalas_utils import (
    calcular_gds15_total,
    interpretar_gds15,
    calcular_katz_total as calcular_katz_total_nuevo,
    interpretar_katz as interpretar_katz_nuevo,
    calcular_lawton_total,
    interpretar_lawton
)

from app.utils.permisos import (
    puede_ver_area,
    puede_crear_area,
    puede_editar_area,
    puede_eliminar_area,
    puede_descargar_pdf_area
)

from . import actividad_social_bp

AREA = "actividad_social"


@actividad_social_bp.route("", methods=["GET"])
@login_required
def actividad_social_lista(paciente_id):
    if not puede_ver_area(current_user, AREA):
        abort(403)
        
    paciente = Paciente.query.get_or_404(paciente_id)

    actividades = ActividadSocial.query.filter_by(
        paciente_id=paciente.id
    ).order_by(ActividadSocial.created_at.desc()).all()

    return render_template(
        "actividad_social/actividad_social_lista.html",
        paciente=paciente,
        actividades=actividades,
        puede_crear=puede_crear_area(current_user, AREA),
        puede_editar=puede_editar_area(current_user, AREA),
        puede_eliminar=puede_eliminar_area(current_user, AREA),
        puede_pdf=puede_descargar_pdf_area(current_user, AREA),
    )


@actividad_social_bp.route("/nueva", methods=["POST"])
@login_required
def actividad_social_nueva(paciente_id):
    if not puede_crear_area(current_user, AREA):
        abort(403)
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
    if not puede_ver_area(current_user, AREA):
        abort(403)
    paciente = Paciente.query.get_or_404(paciente_id)

    actividad = ActividadSocial.query.filter_by(
        id=actividad_id,
        paciente_id=paciente.id
    ).first_or_404()

    seccion = request.args.get("seccion", "datos_generales")

    editable_social = puede_editar_area(current_user, AREA)

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
    salud_mental_form = ActividadSocialSaludMentalForm()
    gds15_form = ActividadSocialGDS15Form()
    katz_form = ActividadSocialKatzForm()
    lawton_brody_form = ActividadSocialLawtonBrodyForm()

    # Bloqueo real de edición por backend
    if request.method == "POST" and not editable_social:
        flash("Esta captura ya está finalizada o no tienes permiso para editarla.", "danger")
        return redirect(url_for(
            "actividad_social.actividad_social_detalle",
            paciente_id=paciente.id,
            actividad_id=actividad.id,
            seccion=seccion
        ))

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
            
        if actividad.salud_mental:
            salud_mental_form.gds_total.data = actividad.salud_mental.gds_total

            salud_mental_form.lawton_telefono.data = actividad.salud_mental.lawton_telefono
            salud_mental_form.lawton_transporte.data = actividad.salud_mental.lawton_transporte
            salud_mental_form.lawton_compras.data = actividad.salud_mental.lawton_compras
            salud_mental_form.lawton_alimentos.data = actividad.salud_mental.lawton_alimentos
            salud_mental_form.lawton_hogar.data = actividad.salud_mental.lawton_hogar
            salud_mental_form.lawton_medicacion.data = actividad.salud_mental.lawton_medicacion
            salud_mental_form.lawton_dinero.data = actividad.salud_mental.lawton_dinero

            salud_mental_form.katz_banio.data = actividad.salud_mental.katz_banio
            salud_mental_form.katz_vestido.data = actividad.salud_mental.katz_vestido
            salud_mental_form.katz_sanitario.data = actividad.salud_mental.katz_sanitario
            salud_mental_form.katz_transferencia.data = actividad.salud_mental.katz_transferencia
            salud_mental_form.katz_continencia.data = actividad.salud_mental.katz_continencia
            salud_mental_form.katz_alimentacion.data = actividad.salud_mental.katz_alimentacion
            salud_mental_form.katz_letra.data = actividad.salud_mental.katz_letra
            
        if actividad.gds15:
            for i in range(1, 16):
                getattr(gds15_form, f"p{i}").data = getattr(actividad.gds15, f"p{i}")

        if actividad.katz:
            katz_form.bano.data = str(actividad.katz.bano) if actividad.katz.bano is not None else None
            katz_form.vestido.data = str(actividad.katz.vestido) if actividad.katz.vestido is not None else None
            katz_form.uso_sanitario.data = str(actividad.katz.uso_sanitario) if actividad.katz.uso_sanitario is not None else None
            katz_form.transferencias.data = str(actividad.katz.transferencias) if actividad.katz.transferencias is not None else None
            katz_form.continencia.data = str(actividad.katz.continencia) if actividad.katz.continencia is not None else None
            katz_form.alimentacion.data = str(actividad.katz.alimentacion) if actividad.katz.alimentacion is not None else None
            katz_form.clasificacion_letra.data = actividad.katz.clasificacion_letra

        if actividad.lawton_brody:
            lawton_brody_form.telefono.data = str(actividad.lawton_brody.telefono) if actividad.lawton_brody.telefono is not None else None
            lawton_brody_form.transporte.data = str(actividad.lawton_brody.transporte) if actividad.lawton_brody.transporte is not None else None
            lawton_brody_form.compras.data = str(actividad.lawton_brody.compras) if actividad.lawton_brody.compras is not None else None
            lawton_brody_form.preparacion_alimentos.data = str(actividad.lawton_brody.preparacion_alimentos) if actividad.lawton_brody.preparacion_alimentos is not None else None
            lawton_brody_form.quehaceres_hogar.data = str(actividad.lawton_brody.quehaceres_hogar) if actividad.lawton_brody.quehaceres_hogar is not None else None
            lawton_brody_form.medicacion.data = str(actividad.lawton_brody.medicacion) if actividad.lawton_brody.medicacion is not None else None
            lawton_brody_form.manejo_dinero.data = str(actividad.lawton_brody.manejo_dinero) if actividad.lawton_brody.manejo_dinero is not None else None

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
        
        
    # =========================
    # SALUD MENTAL
    # =========================
    if editable_social and seccion == "salud_mental" and salud_mental_form.validate_on_submit():
        if not actividad.salud_mental:
            actividad.salud_mental = ActividadSocialSaludMental(
                actividad_social_id=actividad.id
            )
            db.session.add(actividad.salud_mental)

        actividad.salud_mental.gds_total = salud_mental_form.gds_total.data
        actividad.salud_mental.gds_interpretacion = interpretar_gds(
            salud_mental_form.gds_total.data
        )

        actividad.salud_mental.lawton_telefono = salud_mental_form.lawton_telefono.data
        actividad.salud_mental.lawton_transporte = salud_mental_form.lawton_transporte.data
        actividad.salud_mental.lawton_compras = salud_mental_form.lawton_compras.data
        actividad.salud_mental.lawton_alimentos = salud_mental_form.lawton_alimentos.data
        actividad.salud_mental.lawton_hogar = salud_mental_form.lawton_hogar.data
        actividad.salud_mental.lawton_medicacion = salud_mental_form.lawton_medicacion.data
        actividad.salud_mental.lawton_dinero = salud_mental_form.lawton_dinero.data

        actividad.salud_mental.katz_banio = salud_mental_form.katz_banio.data
        actividad.salud_mental.katz_vestido = salud_mental_form.katz_vestido.data
        actividad.salud_mental.katz_sanitario = salud_mental_form.katz_sanitario.data
        actividad.salud_mental.katz_transferencia = salud_mental_form.katz_transferencia.data
        actividad.salud_mental.katz_continencia = salud_mental_form.katz_continencia.data
        actividad.salud_mental.katz_alimentacion = salud_mental_form.katz_alimentacion.data
        actividad.salud_mental.katz_letra = salud_mental_form.katz_letra.data

        actividad.salud_mental.katz_total = calcular_katz_total(
            salud_mental_form.katz_banio.data,
            salud_mental_form.katz_vestido.data,
            salud_mental_form.katz_sanitario.data,
            salud_mental_form.katz_transferencia.data,
            salud_mental_form.katz_continencia.data,
            salud_mental_form.katz_alimentacion.data,
        )

        actividad.salud_mental.katz_interpretacion = interpretar_katz(
            actividad.salud_mental.katz_total
        )

        db.session.commit()

        flash("Salud mental guardada correctamente.", "success")

        accion = request.form.get("accion")
        if accion == "siguiente":
            return redirect(url_for(
                "actividad_social.actividad_social_detalle",
                paciente_id=paciente.id,
                actividad_id=actividad.id,
                seccion="resumen"
            ))

        return redirect(url_for(
            "actividad_social.actividad_social_detalle",
            paciente_id=paciente.id,
            actividad_id=actividad.id,
            seccion="salud_mental"
        ))

    # =========================
    # GDS-15
    # =========================
    if editable_social and seccion == "gds15" and gds15_form.validate_on_submit():
        if not actividad.gds15:
            actividad.gds15 = ActividadSocialGDS15(
                actividad_social_id=actividad.id
            )
            db.session.add(actividad.gds15)

        respuestas = {}

        for i in range(1, 16):
            valor = getattr(gds15_form, f"p{i}").data
            setattr(actividad.gds15, f"p{i}", valor)
            respuestas[f"p{i}"] = valor

        actividad.gds15.puntaje_total = calcular_gds15_total(respuestas)
        actividad.gds15.interpretacion = interpretar_gds15(
            actividad.gds15.puntaje_total
        )

        db.session.commit()

        flash("Escala GDS-15 guardada correctamente.", "success")

        accion = request.form.get("accion")
        if accion == "siguiente":
            return redirect(url_for(
                "actividad_social.actividad_social_detalle",
                paciente_id=paciente.id,
                actividad_id=actividad.id,
                seccion="katz"
            ))

        return redirect(url_for(
            "actividad_social.actividad_social_detalle",
            paciente_id=paciente.id,
            actividad_id=actividad.id,
            seccion="gds15"
        ))
        
    # =========================
    # KATZ
    # =========================
    if editable_social and seccion == "katz" and katz_form.validate_on_submit():
        if not actividad.katz:
            actividad.katz = ActividadSocialKatz(
                actividad_social_id=actividad.id
            )
            db.session.add(actividad.katz)

        actividad.katz.bano = int(katz_form.bano.data) if katz_form.bano.data else None
        actividad.katz.vestido = int(katz_form.vestido.data) if katz_form.vestido.data else None
        actividad.katz.uso_sanitario = int(katz_form.uso_sanitario.data) if katz_form.uso_sanitario.data else None
        actividad.katz.transferencias = int(katz_form.transferencias.data) if katz_form.transferencias.data else None
        actividad.katz.continencia = int(katz_form.continencia.data) if katz_form.continencia.data else None
        actividad.katz.alimentacion = int(katz_form.alimentacion.data) if katz_form.alimentacion.data else None
        actividad.katz.clasificacion_letra = katz_form.clasificacion_letra.data

        actividad.katz.puntaje_total = calcular_katz_total_nuevo(
            actividad.katz.bano,
            actividad.katz.vestido,
            actividad.katz.uso_sanitario,
            actividad.katz.transferencias,
            actividad.katz.continencia,
            actividad.katz.alimentacion
        )

        actividad.katz.interpretacion = interpretar_katz_nuevo(
            actividad.katz.puntaje_total
        )

        db.session.commit()

        flash("Índice de Katz guardado correctamente.", "success")

        accion = request.form.get("accion")
        if accion == "siguiente":
            return redirect(url_for(
                "actividad_social.actividad_social_detalle",
                paciente_id=paciente.id,
                actividad_id=actividad.id,
                seccion="lawton_brody"
            ))

        return redirect(url_for(
            "actividad_social.actividad_social_detalle",
            paciente_id=paciente.id,
            actividad_id=actividad.id,
            seccion="katz"
        ))
        
    # =========================
    # LAWTON Y BRODY
    # =========================
    if editable_social and seccion == "lawton_brody" and lawton_brody_form.validate_on_submit():
        if not actividad.lawton_brody:
            actividad.lawton_brody = ActividadSocialLawtonBrody(
                actividad_social_id=actividad.id
            )
            db.session.add(actividad.lawton_brody)

        actividad.lawton_brody.telefono = int(lawton_brody_form.telefono.data) if lawton_brody_form.telefono.data else None
        actividad.lawton_brody.transporte = int(lawton_brody_form.transporte.data) if lawton_brody_form.transporte.data else None
        actividad.lawton_brody.compras = int(lawton_brody_form.compras.data) if lawton_brody_form.compras.data else None
        actividad.lawton_brody.preparacion_alimentos = int(lawton_brody_form.preparacion_alimentos.data) if lawton_brody_form.preparacion_alimentos.data else None
        actividad.lawton_brody.quehaceres_hogar = int(lawton_brody_form.quehaceres_hogar.data) if lawton_brody_form.quehaceres_hogar.data else None
        actividad.lawton_brody.medicacion = int(lawton_brody_form.medicacion.data) if lawton_brody_form.medicacion.data else None
        actividad.lawton_brody.manejo_dinero = int(lawton_brody_form.manejo_dinero.data) if lawton_brody_form.manejo_dinero.data else None

        actividad.lawton_brody.puntaje_total = calcular_lawton_total(
            actividad.lawton_brody.telefono,
            actividad.lawton_brody.transporte,
            actividad.lawton_brody.compras,
            actividad.lawton_brody.preparacion_alimentos,
            actividad.lawton_brody.quehaceres_hogar,
            actividad.lawton_brody.medicacion,
            actividad.lawton_brody.manejo_dinero
        )

        actividad.lawton_brody.interpretacion = interpretar_lawton(
            actividad.lawton_brody.puntaje_total
        )

        db.session.commit()

        flash("Escala de Lawton y Brody guardada correctamente.", "success")

        accion = request.form.get("accion")
        if accion == "siguiente":
            return redirect(url_for(
                "actividad_social.actividad_social_detalle",
                paciente_id=paciente.id,
                actividad_id=actividad.id,
                seccion="resumen"
            ))

        return redirect(url_for(
            "actividad_social.actividad_social_detalle",
            paciente_id=paciente.id,
            actividad_id=actividad.id,
            seccion="lawton_brody"
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
        editable_social=editable_social,
        puede_editar=puede_editar_area(current_user, AREA),
        puede_eliminar=puede_eliminar_area(current_user, AREA),
        puede_pdf=puede_descargar_pdf_area(current_user, AREA),
        salud_mental_form=salud_mental_form,
        gds15_form=gds15_form,
        katz_form=katz_form,
        lawton_brody_form=lawton_brody_form,
    )


@actividad_social_bp.route("/<int:actividad_id>/hermano/<int:hermano_id>/eliminar", methods=["POST"])
@login_required
def actividad_social_hermano_eliminar(paciente_id, actividad_id, hermano_id):
    if not puede_editar_area(current_user, AREA):
        abort(403)
    hermano = ActividadSocialHermano.query.get_or_404(hermano_id)
    actividad = ActividadSocial.query.filter_by(
        id=actividad_id,
        paciente_id=paciente_id
    ).first_or_404()

    if not puede_eliminar_area(current_user, AREA):
        abort(403)
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
    if not puede_editar_area(current_user, AREA):
        abort(403)
        
    hijo = ActividadSocialHijo.query.get_or_404(hijo_id)
    actividad = ActividadSocial.query.filter_by(
        id=actividad_id,
        paciente_id=paciente_id
    ).first_or_404()

    if not puede_eliminar_area(current_user, AREA):
        abort(403)
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

@actividad_social_bp.route("/<int:actividad_id>/eliminar", methods=["POST"])
@login_required
def actividad_social_eliminar(paciente_id, actividad_id):
    if not puede_editar_area(current_user, AREA):
        abort(403)
        
    actividad = ActividadSocial.query.filter_by(
        id=actividad_id,
        paciente_id=paciente_id
    ).first_or_404()

    if not puede_eliminar_area(current_user, AREA):
        abort(403)
        flash("No tienes permiso para eliminar esta captura.", "danger")
        return redirect(url_for(
            "actividad_social.actividad_social_lista",
            paciente_id=paciente_id
        ))

    db.session.delete(actividad)
    db.session.commit()

    flash("Captura de Actividad Social eliminada correctamente.", "success")
    return redirect(url_for(
        "actividad_social.actividad_social_lista",
        paciente_id=paciente_id
    ))

@actividad_social_bp.route("/<int:actividad_id>/finalizar", methods=["POST"])
@login_required
def actividad_social_finalizar(paciente_id, actividad_id):
    actividad = ActividadSocial.query.filter_by(
        id=actividad_id,
        paciente_id=paciente_id
    ).first_or_404()

    if not puede_editar_area(current_user, AREA):
        abort(403)
        flash("No tienes permiso para finalizar esta captura.", "danger")
        return redirect(url_for(
            "actividad_social.actividad_social_detalle",
            paciente_id=paciente_id,
            actividad_id=actividad_id,
            seccion="resumen"
        ))

    actividad.finalizado = True
    actividad.fecha_finalizado = datetime.utcnow()
    db.session.commit() 

    flash("Actividad social finalizada correctamente.", "success")
    return redirect(url_for(
        "actividad_social.actividad_social_lista",
        paciente_id=paciente_id
    ))