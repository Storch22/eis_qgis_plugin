from qgis.core import (
    QgsProcessing,
    QgsProcessingOutputBoolean,
    QgsProcessingParameterBoolean,
    QgsProcessingParameterMultipleLayers,
)

from eis_qgis_plugin.processing.eis_processing_algorithm import EISProcessingAlgorithm


class EISCheckRasterGrids(EISProcessingAlgorithm):
    def __init__(self) -> None:
        super().__init__()

        self._name = "check_raster_grids"
        self._display_name = "Check raster grids"
        self._group = "Raster Processing"
        self._group_id = "raster_processing"
        self._short_help_string = "Check if raster grids have same CRS, alignment, pixel size and optionally extent."

    def initAlgorithm(self, config=None):
        self.alg_parameters = ["input_raster", "same_extent"]

        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                name=self.alg_parameters[0],
                description="Input rasters",
                layerType=QgsProcessing.TypeRaster,
            )
        )

        self.addParameter(
            QgsProcessingParameterBoolean(
                name=self.alg_parameters[1],
                description="Same extent",
                defaultValue=False,
            )
        )

        self.addOutput(
            QgsProcessingOutputBoolean(name="result", description="Check result")
        )
