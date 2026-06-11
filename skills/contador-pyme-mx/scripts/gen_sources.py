import json

VERIFIED_200 = {  # IDs confirmados en vivo vía web_fetch (HTTP 2xx, devolvieron contenido text/xml)
    "sat_cfdi_xsd_v40", "sat_nomina12_xsd", "sat_pagos20_xsd",
    "sat_retencionpago_v2_xsd", "sat_conta_catalogo_cuentas_11",
}

rows = []
def S(id, institution, name, topics, format, url, local_path,
      geography="nacional", granularity="esquema", year=None,
      confianza="alta", requires_auth=False, auth_tipo=None,
      vigencia_dof=None, url_alt=None, notas=""):
    rows.append({
        "id": id,
        "institution": institution,
        "name": name,
        "year": year,
        "topics": topics,
        "geography": geography,
        "granularity": granularity,
        "format": format,
        "url": url,
        "url_alt": url_alt,
        "local_path": local_path,
        "estado_verificacion": "200_OK" if id in VERIFIED_200 else "pendiente",
        "verificado_en_sesion": id in VERIFIED_200,
        "metodo_verificacion": "web_fetch" if id in VERIFIED_200 else None,
        "confianza": confianza,
        "size_bytes_esperado": None,  # lo rellena verify.py
        "requires_auth": requires_auth,
        "auth_tipo": auth_tipo,
        "vigencia_dof": vigencia_dof,
        "notas": notas,
    })

# ---------------- 1. Esquemas CFDI 4.0 y complementos (SAT) ----------------
S("sat_cfdi_xsd_v40","SAT","CFDI 4.0 — esquema base",["cfdi","factura"],"xsd",
  "http://www.sat.gob.mx/sitio_internet/cfd/4/cfdv40.xsd","esquemas-cfdi/cfdv40.xsd",
  notas="Namespace http://www.sat.gob.mx/cfd/4. Importa catCFDI y tdCFDI.")
S("sat_cfdi_xsd_catcfdi","SAT","CFDI 4.0 — catálogos (catCFDI)",["cfdi","catalogos"],"xsd",
  "http://www.sat.gob.mx/sitio_internet/cfd/catalogos/catCFDI.xsd","esquemas-cfdi/catCFDI.xsd",
  notas="Importado por cfdv40.xsd (cadena de imports confirmada en el XSD base vivo).")
S("sat_cfdi_xsd_tdcfdi","SAT","CFDI 4.0 — tipos de datos (tdCFDI)",["cfdi","catalogos"],"xsd",
  "http://www.sat.gob.mx/sitio_internet/cfd/tipoDatos/tdCFDI/tdCFDI.xsd","esquemas-cfdi/tdCFDI.xsd",
  notas="Importado por cfdv40.xsd.")
S("sat_cfdi_xsd_tfd11","SAT","Timbre Fiscal Digital 1.1",["cfdi","timbre"],"xsd",
  "http://www.sat.gob.mx/sitio_internet/cfd/TimbreFiscalDigital/TimbreFiscalDigitalv11.xsd",
  "esquemas-cfdi/TimbreFiscalDigitalv11.xsd",confianza="media",
  notas="Complemento obligatorio del timbrado. Confirmar ruta/versión con verify.py.")
S("sat_nomina12_xsd","SAT","Complemento Nómina 1.2",["nomina","cfdi"],"xsd",
  "http://www.sat.gob.mx/sitio_internet/cfd/nomina/nomina12.xsd","esquemas-cfdi/nomina12.xsd",
  notas="Namespace http://www.sat.gob.mx/nomina12.")
S("sat_nomina12_catnomina_xsd","SAT","Catálogos Nómina 1.2 (catNomina)",["nomina","catalogos"],"xsd",
  "http://www.sat.gob.mx/sitio_internet/cfd/catalogos/Nomina/catNomina.xsd","esquemas-cfdi/catNomina.xsd",
  notas="Ruta de import declarada dentro de nomina12.xsd.")
S("sat_pagos20_xsd","SAT","Complemento Pagos 2.0 (CRP)",["pagos","cfdi","iva"],"xsd",
  "http://www.sat.gob.mx/sitio_internet/cfd/Pagos/Pagos20.xsd","esquemas-cfdi/Pagos20.xsd",
  notas="Namespace http://www.sat.gob.mx/Pagos20. Unica version valida desde 2023-04.")
S("sat_pagos20_catpagos_xsd","SAT","Catálogos Pagos 2.0 (catPagos)",["pagos","catalogos"],"xsd",
  "http://www.sat.gob.mx/sitio_internet/cfd/catalogos/Pagos/catPagos.xsd","esquemas-cfdi/catPagos.xsd",
  notas="Ruta de import declarada dentro de Pagos20.xsd.")
S("sat_retencionpago_v2_xsd","SAT","CFDI Retenciones e Información de Pagos 2.0",["retenciones","cfdi"],"xsd",
  "http://www.sat.gob.mx/esquemas/retencionpago/2/retencionpagov2.xsd","esquemas-cfdi/retencionpagov2.xsd",
  notas="Documento distinto al CFDI de ingreso. Unica version valida desde 2023-04.")
S("sat_retencionpago_catalogos_xsd","SAT","Catálogos CFDI Retenciones",["retenciones","catalogos"],"xsd",
  "http://www.sat.gob.mx/esquemas/retencionpago/1/catalogos/catRetenciones.xsd",
  "esquemas-cfdi/catRetenciones.xsd",confianza="media",
  notas="Namespace retencionpago/1/catalogos. Confirmar nombre de archivo con verify.py.")
S("sat_cartaporte_31_xsd","SAT","Complemento Carta Porte 3.1",["carta_porte","cfdi"],"xsd",
  "http://www.sat.gob.mx/sitio_internet/cfd/CartaPorte/CartaPorte31.xsd","esquemas-cfdi/CartaPorte31.xsd",
  confianza="media",notas="Obligatorio si el cliente transporta mercancia. Confirmar version vigente (3.1).")
S("sat_anexo20_guia_pdf","SAT","Guía de llenado Anexo 20 (CFDI 4.0)",["cfdi","guia"],"pdf",
  "http://omawww.sat.gob.mx/tramitesyservicios/Paginas/documentos/GuiaAnexo20.pdf","sat-guias/GuiaAnexo20.pdf",
  granularity="norma")
S("sat_nomina_guia_pdf","SAT","Guía de llenado complemento Nómina",["nomina","guia"],"pdf",
  "http://omawww.sat.gob.mx/tramitesyservicios/Paginas/documentos/Guia_llenado_Nomina.pdf","sat-guias/Guia_llenado_Nomina.pdf",
  granularity="norma")
S("sat_cfdi_retenciones_hub","SAT","Hub CFDI Retenciones e info de pagos (XSD/XSLT/catálogos)",["retenciones","cfdi"],"web",
  "http://omawww.sat.gob.mx/tramitesyservicios/Paginas/CFDI_retenciones.htm","sat-guias/cfdi_retenciones_hub.html",
  granularity="portal")

# ---------------- 2. Contabilidad electrónica (SAT esquemas) ----------------
S("sat_conta_catalogo_cuentas_11","SAT","Contab. electrónica — Catálogo de cuentas 1.1",["contabilidad","xml"],"xsd",
  "http://www.sat.gob.mx/esquemas/ContabilidadE/1_1/CatalogoCuentas/CatalogoCuentas_1_1.xsd",
  "esquemas-contabilidad/CatalogoCuentas_1_1.xsd")
S("sat_conta_balanza_13","SAT","Contab. electrónica — Balanza de comprobación 1.3",["contabilidad","balanza"],"xsd",
  "http://www.sat.gob.mx/esquemas/ContabilidadE/1_3/BalanzaComprobacion/BalanzaComprobacion_1_3.xsd",
  "esquemas-contabilidad/BalanzaComprobacion_1_3.xsd",
  url_alt="http://omawww.sat.gob.mx/esquemas/ContabilidadE/1_3/BalanzaComprobacion/BalanzaComprobacion_1_3.xsd",
  notas="Version vigente 1.3 (mirror omawww respondio contenido en busqueda).")
S("sat_conta_polizas_13","SAT","Contab. electrónica — Pólizas del periodo 1.3",["contabilidad","polizas"],"xsd",
  "http://www.sat.gob.mx/esquemas/ContabilidadE/1_3/PolizasPeriodo/PolizasPeriodo_1_3.xsd",
  "esquemas-contabilidad/PolizasPeriodo_1_3.xsd",notas="Version vigente 1.3.")
S("sat_conta_auxctas_11","SAT","Contab. electrónica — Auxiliar de cuentas 1.1",["contabilidad"],"xsd",
  "http://www.sat.gob.mx/esquemas/ContabilidadE/1_1/AuxiliarCtas/AuxiliarCtas_1_1.xsd",
  "esquemas-contabilidad/AuxiliarCtas_1_1.xsd",confianza="media")
S("sat_conta_auxfolios_12","SAT","Contab. electrónica — Auxiliar de folios 1.2",["contabilidad"],"xsd",
  "http://www.sat.gob.mx/esquemas/ContabilidadE/1_1/AuxiliarFolios/AuxiliarFolios_1_2.xsd",
  "esquemas-contabilidad/AuxiliarFolios_1_2.xsd",confianza="media")
S("sat_conta_catparaesq","SAT","Contab. electrónica — CatálogosParaEsqContE",["contabilidad","catalogos"],"xsd",
  "http://www.sat.gob.mx/esquemas/ContabilidadE/1_1/CatalogosParaEsqContE/CatalogosParaEsqContE.xsd",
  "esquemas-contabilidad/CatalogosParaEsqContE.xsd",confianza="media")
S("sat_anexo24_rmf2026","SAT","Anexo 24 RMF 2026 — estándares contab. + código agrupador",["contabilidad","norma","codigo_agrupador"],"pdf",
  "https://www.sat.gob.mx/minisitio/NormatividadRMFyRGCE/documentos2026/rmf/anexos/Anexo_24_RMF2026-13012026.pdf",
  "sat-rmf-2026/Anexo_24_RMF2026.pdf",year=2026,granularity="norma",vigencia_dof="2026-01-13",
  notas="Apartado B = codigo agrupador; C = balanza; D = polizas.")
S("sat_conta_faq","SAT","FAQ y envío de contabilidad electrónica",["contabilidad"],"web",
  "http://omawww.sat.gob.mx/fichas_tematicas/buzon_tributario/Paginas/contabilidad_electronica_preguntas.aspx",
  "sat-guias/contabilidad_faq.html",granularity="portal",
  notas="Fundamento Art. 28 fr. IV CFF; reglas 2.8.1.x.")

# ---------------- 3. RMF / tarifas ISR ----------------
S("sat_anexo8_rmf2026","SAT","Anexo 8 RMF 2026 — Tarifas ISR (mensual y anual)",["isr","tarifas","nomina"],"pdf",
  "https://www.sat.gob.mx/minisitio/NormatividadRMFyRGCE/documentos2026/rmf/anexos/Anexo-8-RMF-2026_DOF-28122025.pdf",
  "sat-rmf-2026/Anexo-8-RMF-2026.pdf",year=2026,granularity="norma",vigencia_dof="2025-12-28",
  notas="Factor de actualizacion 1.1321. Tarifa Art.96 (mensual) y Art.152 (anual).")
S("sat_rmf2026_anexos_index","SAT","Índice de anexos RMF 2026 (minisitio)",["rmf","norma"],"web",
  "https://www.sat.gob.mx/minisitio/NormatividadRMFyRGCE/documentos2026/rmf/anexos/",
  "sat-rmf-2026/index.html",year=2026,granularity="portal",
  notas="Cuelgan Anexos 1-A, 4, 5, 6, 8, 15, 24, 25, etc.")

# ---------------- 4. Servicios / portales SAT (con autenticación) ----------------
S("sat_descarga_masiva_portal","SAT","Descarga masiva CFDI — página oficial (WSDL)",["cfdi","conciliacion","descarga_masiva"],"web",
  "https://www.sat.gob.mx/consultas/42968/consulta-y-recuperacion-de-comprobantes-(nuevo)",
  "sat-servicios/descarga_masiva.html",granularity="servicio",
  notas="La pagina es publica; el servicio requiere e.firma. Doc en seccion 'Material adicional'.")
S("sat_dm_autenticacion_svc","SAT","Descarga masiva — endpoint Autenticación",["cfdi","descarga_masiva","soap"],"soap",
  "https://cfdidescargamasivasolicitud.clouda.sat.gob.mx/Autenticacion/Autenticacion.svc",
  None,granularity="servicio",requires_auth=True,auth_tipo="efirma",confianza="media")
S("sat_dm_solicita_svc","SAT","Descarga masiva — endpoint Solicitud",["cfdi","descarga_masiva","soap"],"soap",
  "https://cfdidescargamasivasolicitud.clouda.sat.gob.mx/SolicitaDescargaService.svc",
  None,granularity="servicio",requires_auth=True,auth_tipo="efirma",confianza="media")
S("sat_dm_verifica_svc","SAT","Descarga masiva — endpoint Verificación",["cfdi","descarga_masiva","soap"],"soap",
  "https://cfdidescargamasivasolicitud.clouda.sat.gob.mx/VerificaSolicitudDescargaService.svc",
  None,granularity="servicio",requires_auth=True,auth_tipo="efirma",
  notas="Endpoint confirmado en documentacion oficial del servicio.")
S("sat_dm_descarga_svc","SAT","Descarga masiva — endpoint Descarga",["cfdi","descarga_masiva","soap"],"soap",
  "https://cfdidescargamasiva.clouda.sat.gob.mx/DescargaMasivaService.svc",
  None,granularity="servicio",requires_auth=True,auth_tipo="efirma",confianza="media")
S("sat_consulta_cfdi_svc","SAT","Validar estatus CFDI (vigente/cancelado)",["cfdi","validacion","soap"],"soap",
  "https://consultaqr.facturaelectronica.sat.gob.mx/ConsultaCFDIService.svc?wsdl",
  None,granularity="servicio",confianza="media",
  notas="Servicio publico, sin e.firma. Devuelve estado del comprobante.")
S("sat_diot_plataforma","SAT","Plataforma DIOT (presentación)",["diot","iva"],"web",
  "https://pstcdi.clouda.sat.gob.mx","sat-servicios/diot.html",granularity="servicio",
  requires_auth=True,auth_tipo="contrasena_o_efirma",vigencia_dof="2025-08-01",
  notas="Obligatoria desde 2025-08-01 (Comunicado 42/2025). Layout .txt pipe, UTF-8. Fundamento Art.32 fr.VIII LIVA.")
S("sat_opinion_32d","SAT","Opinión de cumplimiento 32-D (SAT)",["32d","cumplimiento"],"web",
  "https://www.sat.gob.mx/consultas/20777/consulta-tu-opinion-de-cumplimiento-de-obligaciones-fiscales",
  "sat-servicios/opinion_32d.html",granularity="servicio",requires_auth=True,auth_tipo="contrasena_o_efirma",
  notas="Art.32-D CFF; regla 2.1.36; ficha 1/CFF. Vigencia 30 dias (gral) / 3 meses (estimulos).")
S("sat_portal_home","SAT","Portal SAT (Calendario, Declaración Anual, Datos abiertos)",["calendario","anual","portal"],"web",
  "https://www.sat.gob.mx","sat-servicios/portal_sat.html",granularity="portal",
  notas="Secciones Calendario y Declaracion Anual cuelgan de aqui; rutas directas cambian por temporada.")

# ---------------- 5. Padrones / datos abiertos ----------------
S("sat_donatarias_datosabiertos","SAT","Donatarias autorizadas — datos abiertos",["donatarias","datos_abiertos"],"csv",
  "https://www.sat.gob.mx/minisitio/DonatariasAutorizadas/padron_datos_abiertos.html",
  "sat-padrones/donatarias.html",granularity="dataset",
  notas="Donativos, ingresos, erogaciones por donataria (SHCP/SAT).")
S("sat_padron_import_export","SAT","Padrón de importadores / exportadores",["padron","comercio_exterior"],"web",
  "https://www.sat.gob.mx/minisitio/PadronImportadoresExportadores/index.html",
  "sat-padrones/padron_import_export.html",granularity="dataset",
  notas="Activos/suspendidos con fecha de corte + importadores de canasta basica.")
S("datosgobmx_sat_org","SHCP/SAT","Datasets SAT en datos.gob.mx",["datos_abiertos"],"web",
  "https://datos.gob.mx/busca/organization/sat","datos-abiertos/datos_gob_sat.html",
  granularity="dataset",confianza="media",notas="Hub de datasets publicados por el SAT.")

# ---------------- 6. Banxico (tipo de cambio) ----------------
S("banxico_sie_api_base","Banxico","SIE API REST — base",["tipo_cambio","api"],"api_json",
  "https://www.banxico.org.mx/SieAPIRest/service/v1/","banxico/README.md",granularity="api",
  requires_auth=True,auth_tipo="token",
  notas="Requiere token gratuito. Header alterno: Bmx-Token.")
S("banxico_sie_token","Banxico","SIE API — solicitud de token",["tipo_cambio","api"],"web",
  "https://www.banxico.org.mx/SieAPIRest/service/v1/token","banxico/token.html",granularity="portal",
  notas="Genera el token para consumir las series.")
S("banxico_sie_catalogoseries","Banxico","SIE API — catálogo de series",["tipo_cambio","api"],"api_json",
  "https://www.banxico.org.mx/SieAPIRest/service/v1/doc/catalogoSeries","banxico/catalogoSeries.json",
  granularity="api",notas="Confirma SF43718 (FIX) y SF60653 (liquidacion).")
S("banxico_fix_sf43718","Banxico","FIX SF43718 — TC para solventar obligaciones (determinación)",["tipo_cambio","cfdi"],"api_json",
  "https://www.banxico.org.mx/SieAPIRest/service/v1/series/SF43718/datos/oportuno",
  "banxico/SF43718_fix.json",granularity="api",requires_auth=True,auth_tipo="token",
  notas="ESTE es el TC para conversion USD->MXN en CFDI. Endpoint requiere ?token=.")
S("banxico_liquidacion_sf60653","Banxico","SF60653 — TC fecha de liquidación",["tipo_cambio"],"api_json",
  "https://www.banxico.org.mx/SieAPIRest/service/v1/series/SF60653/datos/oportuno",
  "banxico/SF60653_liquidacion.json",granularity="api",requires_auth=True,auth_tipo="token")

# ---------------- 7. INEGI (INPC / UMA) ----------------
S("inegi_inpc_tema","INEGI","INPC — tema/landing",["inpc","inflacion"],"web",
  "https://www.inegi.org.mx/temas/inpc/","inegi/inpc_tema.html",granularity="portal",
  notas="Base 2a quincena julio 2018 = 100.")
S("inegi_inpc_indices_export","INEGI","INPC — índices de precios (export CSV histórico)",["inpc","inflacion"],"csv",
  "https://www.inegi.org.mx/app/indicesdeprecios/Estructura.aspx?idEstructura=112001300040",
  "inegi/inpc_historico.csv",granularity="dataset",
  notas="Para actualizaciones por inflacion Art.17-A CFF. Exporta serie mensual.")
S("inegi_api_indicadores","INEGI","INEGI API de Indicadores (token)",["inpc","api"],"web",
  "https://www.inegi.org.mx/servicios/api_indicadores.html","inegi/api_indicadores.html",
  granularity="api",requires_auth=True,auth_tipo="token",
  notas="Registra token; toma el ID de indicador del INPC del catalogo de esta pagina.")
S("banxico_inpc_cp154","Banxico","INPC (alterno) — cuadro SIE CP154",["inpc"],"web",
  "https://www.banxico.org.mx/SieInternet/consultarDirectorioInternetAction.do?accion=consultarCuadro&idCuadro=CP154",
  "inegi/inpc_banxico_cp154.html",granularity="dataset",
  notas="Util si ya consumes Banxico SIE.")
S("inegi_uma_tema","INEGI","UMA — tema/valores",["uma","valores"],"web",
  "https://www.inegi.org.mx/temas/uma/","inegi/uma.html",granularity="portal",year=2026,
  vigencia_dof="2026-01-09",notas="UMA 2026: 117.31 diario / 3566.22 mensual / 42794.64 anual. Vigente 1-feb-2026.")

# ---------------- 8. DOF / CONASAMI ----------------
S("dof_salario_minimo_2026","DOF/CONASAMI","Resolución salarios mínimos 2026",["salario_minimo","nomina"],"web",
  "https://www.dof.gob.mx/nota_detalle.php?codigo=5775534&fecha=09/12/2025",
  "dof/salario_minimo_2026.html",granularity="norma",year=2026,vigencia_dof="2025-12-09",
  notas="General 315.04 / ZLFN 440.87 por jornada diaria. Vigente 1-ene-2026.")
S("dof_home","DOF","Diario Oficial de la Federación — buscador",["dof","norma"],"web",
  "https://www.dof.gob.mx","dof/index.html",granularity="portal",
  notas="Busqueda de notas por codigo/fecha.")

# ---------------- 9. IMSS / INFONAVIT / STPS ----------------
S("imss_32d_buzon","IMSS","Opinión de cumplimiento 32-D (IMSS)",["32d","imss","cumplimiento"],"web",
  "https://buzon.imss.gob.mx/opinioncumplimiento/","imss/opinion_32d.html",granularity="servicio",
  requires_auth=True,auth_tipo="efirma",notas="Requiere NPR con >=1 trabajador.")
S("imss_sua","IMSS","SUA — Sistema Único de Autodeterminación",["imss","cuotas","nomina"],"web",
  "http://www.imss.gob.mx/patrones/sua","imss/sua.html",granularity="servicio",
  notas="Aplicacion oficial de calculo/cedulas IMSS-INFONAVIT.")
S("imss_idse","IMSS","IDSE — movimientos afiliatorios",["imss","afiliacion","nomina"],"web",
  "https://idse.imss.gob.mx/","imss/idse.html",granularity="servicio",requires_auth=True,auth_tipo="efirma",
  notas="Altas/bajas/modif. de salario (5 dias habiles).")
S("infonavit_portal","INFONAVIT","Portal INFONAVIT (constancia / 32-D)",["infonavit","32d","cumplimiento"],"web",
  "https://www.infonavit.org.mx/","infonavit/portal.html",granularity="servicio",
  notas="Aportacion 5%; opinion de cumplimiento; autorizar 'hacer publica' la opinion.")
S("stps_repse","STPS","REPSE — registro de servicios especializados",["repse","subcontratacion","laboral"],"web",
  "https://repse.stps.gob.mx/","stps/repse.html",granularity="servicio",requires_auth=True,auth_tipo="registro",
  notas="Sin REPSE se cae deduccion ISR y acreditamiento IVA del subcontratado (reforma 2021).")

# ---------------- 10. Leyes federales (Cámara de Diputados) ----------------
S("dip_lisr","Diputados","Ley del ISR (LISR) — texto vigente",["isr","ley"],"pdf",
  "https://www.diputados.gob.mx/LeyesBiblio/pdf/LISR.pdf","leyes-federales/LISR.pdf",granularity="ley",
  notas="FALTANTE en tu corpus. Patron /pdf/ confirmado (puede redirigir a portalhcd).")
S("dip_liva","Diputados","Ley del IVA (LIVA) — texto vigente",["iva","ley"],"pdf",
  "https://www.diputados.gob.mx/LeyesBiblio/pdf/LIVA.pdf","leyes-federales/LIVA.pdf",granularity="ley",
  notas="FALTANTE. URL devolvio contenido en busqueda.")
S("dip_lieps","Diputados","Ley del IEPS (LIEPS) — texto vigente",["ieps","ley"],"pdf",
  "https://www.diputados.gob.mx/LeyesBiblio/pdf/LIEPS.pdf","leyes-federales/LIEPS.pdf",granularity="ley",
  notas="FALTANTE.")
S("dip_cff","Diputados","Código Fiscal de la Federación (CFF)",["cff","ley"],"pdf",
  "https://www.diputados.gob.mx/LeyesBiblio/pdf/CFF.pdf","leyes-federales/CFF.pdf",granularity="ley",
  notas="Ya lo tienes; incluido por completitud.")
S("dip_lft","Diputados","Ley Federal del Trabajo (LFT)",["lft","laboral","ley"],"pdf",
  "https://www.diputados.gob.mx/LeyesBiblio/pdf/LFT.pdf","leyes-federales/LFT.pdf",granularity="ley",
  notas="Ya lo tienes. Reforma 'vacaciones dignas' (12 dias 1er anio).")
S("dip_lss","Diputados","Ley del Seguro Social (LSS)",["lss","imss","ley"],"pdf",
  "https://www.diputados.gob.mx/LeyesBiblio/pdf/LSS.pdf","leyes-federales/LSS.pdf",granularity="ley",
  notas="Ya lo tienes. % de cuotas son estatutarios (no hay 'tarifa' PDF).")
S("dip_linfonavit","Diputados","Ley del INFONAVIT",["infonavit","ley"],"pdf",
  "https://www.diputados.gob.mx/LeyesBiblio/pdf/LINFONAVIT.pdf","leyes-federales/LINFONAVIT.pdf",
  granularity="ley",confianza="media",notas="Confirmar nombre exacto del PDF en el indice.")
S("dip_reglamentos","Diputados","Reglamentos (RCFF, RLISR, RLIVA) — índice",["reglamentos","ley"],"web",
  "https://www.diputados.gob.mx/LeyesBiblio/index.htm","leyes-federales/index.html",granularity="portal",
  confianza="media",notas="Los reglamentos usan /regley/Reg_*_<fecha>.pdf (nombre con fecha cambia). Descargar desde el indice.")

# dump
out = "/home/claude/contador-pyme-mx/sources.json"
with open(out, "w", encoding="utf-8") as f:
    json.dump(rows, f, ensure_ascii=False, indent=2)
print("entries:", len(rows))
print("200_OK:", sum(1 for r in rows if r["estado_verificacion"]=="200_OK"))
print("requires_auth:", sum(1 for r in rows if r["requires_auth"]))
print("confianza_media:", sum(1 for r in rows if r["confianza"]=="media"))
