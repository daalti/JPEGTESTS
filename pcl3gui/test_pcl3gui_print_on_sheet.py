import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Simple print job on sheet PCL3GUI file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid:LFPSWQAA-4580
    +timeout:300
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:printOnsheet.pcl=c7d2cfb9f1753ec458941cc0a18f704c641773ad161adef0d93a5e1d7be5af19
    +name:test_pcl3gui_print_on_sheet
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL3GUI
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pcl3gui_print_on_sheet
        +guid:8c673f34-c14e-4792-94c9-c2a625497b90
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL3GUI&DeviceClass=MFP

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pcl3gui_print_on_sheet(setup_teardown, printjob, outputsaver, tray):
    default = tray.get_default_source()
    if tray.is_size_supported('iso_a4_210x297mm', default):
        tray.configure_tray(default, 'iso_a4_210x297mm', 'stationery')

    printjob.print_verify('c7d2cfb9f1753ec458941cc0a18f704c641773ad161adef0d93a5e1d7be5af19', timeout=300)
    outputsaver.save_output()

    logging.info("PCL3GUI print on sheet successfully")
