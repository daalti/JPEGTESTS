import pytest
import logging
from dunetuf.print.print_common_types import MediaSize, MediaType


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:C52178010 Simple print job of Jpeg TestSuite parrots Progressive Interlaced Page from *parrots_Progressive_Interlaced.jpg file
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-17136
    +timeout:660
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:parrots_Progressive_Interlaced.jpg=dfcaa88adf10d6833f97280b5a58893db02845db6c41495cd324ccb1145bda9a
    +test_classification:System
    +name:test_jpeg_testsuite_parrots_Progressive_Interlaced
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_testsuite_parrots_Progressive_Interlaced
        +guid:5dc2bce6-1d50-44ef-9a9f-205e344d1cc6
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG
    +overrides:
        +Home:
            +is_manual:False
            +timeout:660
            +test:
                +dut:
                    +type:Engine
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_jpeg_testsuite_parrots_Progressive_Interlaced(setup_teardown, printjob, outputsaver, tray, print_emulation, print_mapper, udw, reset_tray):
    # Print file size : width 10.67 inches and height 7.11 inches
    default = tray.get_default_source()
    if tray.is_size_supported('anycustom', default):
        tray.configure_tray(default, 'anycustom', 'stationery')
    elif tray.is_size_supported('any', default):
        tray_test_name = print_mapper.get_media_input_test_name(default)
        print_emulation.tray.setup_tray(tray_test_name, MediaSize.Letter.name, MediaType.Plain.name)
        tray.configure_tray(default, 'any', 'any')
    else:
        tray.configure_tray(default, 'custom', 'stationery')
    outputsaver.validate_crc_tiff(udw) 
    printjob.print_verify('dfcaa88adf10d6833f97280b5a58893db02845db6c41495cd324ccb1145bda9a', timeout=600)
    outputsaver.save_output()
    logging.info("Get crc value for the current print job")
    Current_crc_value = outputsaver.get_crc() 
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"
    tray.reset_trays()
    logging.info("JPEG TestSuite parrots Progressive Interlaced Page - Print job completed successfully")
