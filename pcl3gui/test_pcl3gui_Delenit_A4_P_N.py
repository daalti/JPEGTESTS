import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job of pcl3Gui_Delenit_A4_P_N
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-18107
    +timeout:300
    +asset:PDL_Print
    +delivery_team:LFP 
    +feature_team:LFP_PrintWorkflows
    +test_framework:TUF
    +external_files:Delenit_A4_P_N.PCL=46f5bd9eb75c54f928c1b3d79da43ead733944bfd31d604cc9698388a5e0deb8
    +test_classification:System
    +name:test_pcl3Gui_Delenit_A4_P_N
    +test:
        +title:test_pcl3Gui_Delenit_A4_P_N
        +guid:a84487d6-0fb3-11eb-bc0c-4b3cf9662293
        +dut:
            +type:Simulator, Emulator
            +configuration: DocumentFormat=PCL3GUI
$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pcl3Gui_Delenit_A4_P_N(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    if tray.is_size_supported('iso_a4_210x297mm', default):
        tray.configure_tray(default, 'iso_a4_210x297mm', 'stationery')

    printjob.print_verify('46f5bd9eb75c54f928c1b3d79da43ead733944bfd31d604cc9698388a5e0deb8', timeout=300)
    outputsaver.save_output()
    tray.reset_trays()

    logging.info("Pcl3Gui Delenit_A4_P_N- Print job completed successfully")
