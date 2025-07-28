import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of urf a4
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-15734
    +timeout:300
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:A4.urf=2b0adec1b1c778ae0f84c76a23f21347a055d2b39ed5b2ee09cd731d321dda06
    +name:test_urf_a4
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_a4
        +guid:6f7819b0-3482-11eb-92ac-3f6ed8f0350d
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_a4(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    if tray.is_size_supported('iso_a4_210x297mm', default):
        tray.configure_tray(default, 'iso_a4_210x297mm', 'stationery')
    printjob.print_verify('2b0adec1b1c778ae0f84c76a23f21347a055d2b39ed5b2ee09cd731d321dda06', timeout=300)
    outputsaver.save_output()
    tray.reset_trays()    
    #switch back to default operation mode
    outputsaver.operation_mode('NONE')
    #collect and verify crc
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
    logging.info("URF A4 - Print job completed successfully")