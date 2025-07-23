import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of pwg ph only print quality-1 page from *PwgPhOnly-PrintQuality-1.pwg file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-13665
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:PwgPhOnly-PrintQuality-1.pwg=fea7f378d9725227da00f5e9c5b0f79a1f9dbca2f11990ecc6cae595fd840279
    +name:test_pwg_ph_only_print_quality_1_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PWGRaster
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pwg_ph_only_print_quality_1_page
        +guid:cfa0503f-fbf5-4ea8-9ac8-a8f1d3de575f
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PWGRaster

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pwg_ph_only_print_quality_1_page(setup_teardown, printjob, outputsaver):
    printjob.print_verify('fea7f378d9725227da00f5e9c5b0f79a1f9dbca2f11990ecc6cae595fd840279')
    outputsaver.save_output()

    logging.info("PWG Ph Only Print Quality-1 - Print job completed successfully")
