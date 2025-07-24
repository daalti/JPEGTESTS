import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using jbdtest.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:jbdtest.obj=07442f34fd81b7c60e3420689864ad85d48d9fe6e4d6c63ed68978ac04c0a799
    +test_classification:System
    +name: test_pcl5_pcl_fontdes_ftsdisk_jbdtest
    +test:
        +title: test_pcl5_pcl_fontdes_ftsdisk_jbdtest
        +guid:5546d4b9-64e6-4201-a7e7-9ce0cdca867f
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_fontdes_ftsdisk_jbdtest(setup_teardown, printjob, outputsaver):
    printjob.print_verify('07442f34fd81b7c60e3420689864ad85d48d9fe6e4d6c63ed68978ac04c0a799', timeout=600)
    outputsaver.save_output()
