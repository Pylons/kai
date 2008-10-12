<%inherit file="layout.mako" />
<%def name="title()">${parent.title()} - Error ${c.code}</%def>
${c.message}