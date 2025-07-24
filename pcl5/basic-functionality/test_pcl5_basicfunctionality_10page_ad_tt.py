import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 basicfunctionality using 10Page_ad_tt.obj
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:240
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:10Page-ad_tt.obj=b7d255091ccaa3c71d2fc24d68974baa4f5ec67fdad28322f98190348df48f80
    +test_classification:System
    +name: test_pcl5_basicfunctionality_10page_ad_tt
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_basicfunctionality_10page_ad_tt
        +guid:69e94cec-09d6-4839-b828-2d14ed1e5e50
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5
    +overrides:
        +Enterprise:
            +is_manual:False
            +timeout:600
            +test:
                +dut:
                    +type:Emulator
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pcl5_basicfunctionality_10page_ad_tt(setup_teardown, printjob,udw,outputsaver):
    outputsaver.validate_crc_tiff(udw)
    printjob.print_verify('b7d255091ccaa3c71d2fc24d68974baa4f5ec67fdad28322f98190348df48f80', timeout=180)
    outputsaver.save_output()
    outputsaver.operation_mode('NONE')
    logging.info("Get crc value for the current print job")
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
