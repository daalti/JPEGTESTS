import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 testfiles using TeenyWeenyDots.pcl
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:TeenyWeenyDots.pcl=31e7a3b3576bc159853ad1f6703a92b2671e86da1c349be2b84ec9d68f6c5299
    +test_classification:System
    +name: test_pcl5_testfiles_vector_teenyweenydots
    +test:
        +title: test_pcl5_testfiles_vector_teenyweenydots
        +guid:d5f595fd-e65f-4233-9170-55ea50f35cc4
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_testfiles_vector_teenyweenydots(setup_teardown, printjob, outputsaver):
    printjob.print_verify('31e7a3b3576bc159853ad1f6703a92b2671e86da1c349be2b84ec9d68f6c5299', timeout=600)
    outputsaver.save_output()
