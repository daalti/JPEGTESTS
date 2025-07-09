import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:simple print job of jpeg file of photoimages smalljpg imge26 medium
    +test_tier:1
    +is_manual:False
    +reqid:DUNEPA-126
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:photoimages_smalljpg_imge26_medium.jpg=427585da86657e376a639a6259002ef94d72006de5c4caa897f60a1de3ddfe84
    +test_classification:System
    +name:test_jpeg_photoimages_smalljpg_imge26_medium
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_photoimages_smalljpg_imge26_medium
        +guid:2790d5b3-f779-467e-9e19-2d4f8e1cabea
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_jpeg_photoimages_smalljpg_imge26_medium(setup_teardown, printjob, outputsaver, tray):
    tray.reset_trays()
    
    printjob.print_verify('427585da86657e376a639a6259002ef94d72006de5c4caa897f60a1de3ddfe84')
    outputsaver.save_output()

    logging.info("Jpeg file example photoimages smalljpg imge26 medium - Print job completed successfully")
