import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:C52178023 Simple print job of Envelope Monarch Color urf from *Envelope_Monarch_Color.urf file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-15734
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:Envelope_Monarch_Color.urf=dbe822deee5bea3b67360a67069da2a668b11cba4c122bcdda6f7b65c94512d0
    +name:test_urf_envelope_monarch_color_page
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:URF
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_urf_envelope_monarch_color_page
        +guid:295644b7-01aa-4f22-9a2d-362d95eef6e5
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=URF
    +overrides:
        +Home:
            +is_manual:False
            +timeout:300
            +test:
                +dut:
                    +type:Engine
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_urf_envelope_monarch_color_page(setup_teardown, printjob, outputsaver, tray, udw, reset_tray):
    default = tray.get_default_source()
    if tray.is_size_supported('na_monarch_3.875x7.5in', default):
        tray.configure_tray(default, 'na_monarch_3.875x7.5in', 'stationery')
    outputsaver.validate_crc_tiff(udw)
    printjob.print_verify('dbe822deee5bea3b67360a67069da2a668b11cba4c122bcdda6f7b65c94512d0')
    outputsaver.save_output()
    logging.info("Get crc value for the current print job")
    Current_crc_value = outputsaver.get_crc() 
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
    tray.reset_trays()

    logging.info("URF Envelope Monarch Color page - Print job completed successfully")
