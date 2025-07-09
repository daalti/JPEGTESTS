import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Print large jpeg job
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-228793
    +timeout:200
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:large_image.jpg=40c7bdccc3b536ed31a43208fa935333481533bd65f37fe7dec9a6cf24dc9078
    +test_classification:System
    +name:test_jpeg_largefile
    +test:
        +title:test_jpeg_largefile
        +guid:0d74a1b0-1e54-452e-a122-ab047e0ad432
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG & DigitalStorageType=HardDisk & EngineFirmwareFamily=Canon


$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_jpeg_largefile(setup_teardown, printjob, outputsaver, tray, udw):
    tray.reset_trays()
    outputsaver.validate_crc_tiff(udw)
    printjob.print_verify('40c7bdccc3b536ed31a43208fa935333481533bd65f37fe7dec9a6cf24dc9078')
    outputsaver.save_output()
    logging.info("Get crc value for the current print job")
    Current_crc_value = outputsaver.get_crc()
    logging.info("Validate current crc with master crc")
    assert outputsaver.verify_pdl_crc(Current_crc_value), "fail on crc mismatch"