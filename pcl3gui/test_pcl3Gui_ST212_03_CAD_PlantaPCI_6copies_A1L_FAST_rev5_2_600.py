import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Print job file ST212-03-CAD-PlantaPCI-6copies-A1L-FAST-rev5_-2_600.prn and verify
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-61462
    +timeout:800
    +asset:PDL_Print
    +test_framework:TUF
    +delivery_team:LFP
    +feature_team:LFP_PrintWorkflows
    +external_files:ST212-03-CAD-PlantaPCI-6copies-A1L-FAST-rev5_-2_600.prn=28464adb04de938485bcc320bafc6286e330e0670aba47c35574b871922036ec
    +test_classification:System
    +name:test_pcl3Gui_ST212_03_CAD_PlantaPCI_6copies_A1L_FAST_rev5_2_600
    +test:
        +title:test_pcl3Gui_ST212_03_CAD_PlantaPCI_6copies_A1L_FAST_rev5_2_600
        +guid:434c4c88-8afb-4e80-9aa8-51aaf7d389ce
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=PCL3GUI&EngineFirmwareFamily=Maia
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pcl3Gui_ST212_03_CAD_PlantaPCI_6copies_A1L_FAST_rev5_2_600(setup_teardown, printjob, outputsaver, tcl, ssh, scp):

    # CRC will be calculated using the payload of all the RasterDatas
    outputsaver.operation_mode('CRC')

    printjob.print_verify('28464adb04de938485bcc320bafc6286e330e0670aba47c35574b871922036ec', 'SUCCESS', 800, 1)
    logging.info("ST212-03-CAD-PlantaPCI-6copies-A1L-FAST-rev5_-2_600.prn - Print job completed successfully")

    expected_crc = ["0x6d2beb27", "0x6d2beb27", "0x6d2beb27", "0x6d2beb27", "0x6d2beb27", "0x6d2beb27"]

    # Read and verify that obtained checksums are the expected ones
    outputsaver.save_output()
    outputsaver.verify_output_crc(expected_crc)
    logging.info("ST212-03-CAD-PlantaPCI-6copies-A1L-FAST-rev5_-2_600.prn - Print job completed successfully")
