import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 testfiles using dwnldBitmap.pcl
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:dwnldBitmap.pcl=0ea6f95bfb0874f3553ffcb74da7bb17b7ea0068d89c4e1a26c427d237548526
    +test_classification:System
    +name: test_pcl5_testfiles_text_dwnldbitmap
    +test:
        +title: test_pcl5_testfiles_text_dwnldbitmap
        +guid:a76bfa00-252c-4266-ae4a-efdc29c2a757
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_testfiles_text_dwnldbitmap(setup_teardown, printjob, outputsaver):
    printjob.print_verify('0ea6f95bfb0874f3553ffcb74da7bb17b7ea0068d89c4e1a26c427d237548526', timeout=600)
    outputsaver.save_output()
