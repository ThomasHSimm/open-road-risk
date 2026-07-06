<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis version="3.34" styleCategories="Symbology">
  <renderer-v2 type="graduatedSymbol" attr="crude_rate_per_million_vkm" graduatedMethod="GraduatedColor" symbollevels="0">
    <ranges>
      <range lower="0" upper="1" symbol="0" label="0-1"/>
      <range lower="1" upper="5" symbol="1" label="1-5"/>
      <range lower="5" upper="10" symbol="2" label="5-10"/>
      <range lower="10" upper="25" symbol="3" label="10-25"/>
      <range lower="25" upper="50" symbol="4" label="25-50"/>
      <range lower="50" upper="1000000000" symbol="5" label="50+"/>
    </ranges>
    <symbols>
      <symbol name="0" type="line"><layer class="SimpleLine"><Option type="Map"><Option name="line_color" value="241,245,249,255"/><Option name="line_width" value="0.18"/></Option></layer></symbol>
      <symbol name="1" type="line"><layer class="SimpleLine"><Option type="Map"><Option name="line_color" value="186,230,253,255"/><Option name="line_width" value="0.20"/></Option></layer></symbol>
      <symbol name="2" type="line"><layer class="SimpleLine"><Option type="Map"><Option name="line_color" value="125,211,252,255"/><Option name="line_width" value="0.22"/></Option></layer></symbol>
      <symbol name="3" type="line"><layer class="SimpleLine"><Option type="Map"><Option name="line_color" value="56,189,248,255"/><Option name="line_width" value="0.25"/></Option></layer></symbol>
      <symbol name="4" type="line"><layer class="SimpleLine"><Option type="Map"><Option name="line_color" value="2,132,199,255"/><Option name="line_width" value="0.30"/></Option></layer></symbol>
      <symbol name="5" type="line"><layer class="SimpleLine"><Option type="Map"><Option name="line_color" value="12,74,110,255"/><Option name="line_width" value="0.38"/></Option></layer></symbol>
    </symbols>
  </renderer-v2>
</qgis>
