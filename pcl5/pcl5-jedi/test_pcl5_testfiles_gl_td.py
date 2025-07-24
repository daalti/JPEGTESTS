import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 testfiles using td.pcl
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:td.pcl=2176ba6c69115fedbc388b8fca98ccdc9075786d0be308a02ff788d242e0434c
    +test_classification:System
    +name: test_pcl5_testfiles_gl_td
    +test:
        +title: test_pcl5_testfiles_gl_td
        +guid:300e42dc-822b-4f87-978f-cf04578e5413
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_testfiles_gl_td(setup_teardown, printjob, outputsaver):
    printjob.print_verify('2176ba6c69115fedbc388b8fca98ccdc9075786d0be308a02ff788d242e0434c', timeout=600)
    outputsaver.save_output()
