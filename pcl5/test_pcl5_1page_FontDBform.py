import pytest
import logging

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: unitoffice.prn is a customer escalation file where some text are bold font  and other are printing in regular font
    +test_tier: 1
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-211735
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:unit1office.prn=a6cdcd7b0413452bb3ddb814008c26c845a8dce630a23fc9c411ee091add7beb
    +test_classification:System
    +name: test_pcl5_1page_FontDBform
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_pcl5_1page_FontDBform
        +guid:61de0785-9e2f-40df-a4d3-a62a9b2dd84f
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_1page_FontDBform(setup_teardown, printjob,udw,outputsaver, outputverifier,tray):
    outputsaver.validate_crc_tiff(udw)
    default = tray.get_default_source()
    if tray.is_size_supported('iso_ra4_215x305mm', default):
        tray.configure_tray(default, 'iso_ra4_215x305mm', 'stationery')
    printjob.print_verify('a6cdcd7b0413452bb3ddb814008c26c845a8dce630a23fc9c411ee091add7beb')
    outputverifier.save_and_parse_output()
    outputsaver.save_output()
    outputsaver.operation_mode('NONE')
    logging.info("Get crc value for the current print job")
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"

