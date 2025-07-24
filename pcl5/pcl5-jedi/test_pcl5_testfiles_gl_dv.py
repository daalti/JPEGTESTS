import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 testfiles using dv.pcl
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:dv.pcl=32b36edaa7e05baf9c8325f59a955dabbd39a702b6b20a31774fe093c42f5272
    +test_classification:System
    +name: test_pcl5_testfiles_gl_dv
    +test:
        +title: test_pcl5_testfiles_gl_dv
        +guid:bb6b5f73-6285-4ef2-9414-cf40285804f9
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_testfiles_gl_dv(setup_teardown, printjob, outputsaver):
    printjob.print_verify('32b36edaa7e05baf9c8325f59a955dabbd39a702b6b20a31774fe093c42f5272', timeout=600)
    outputsaver.save_output()
