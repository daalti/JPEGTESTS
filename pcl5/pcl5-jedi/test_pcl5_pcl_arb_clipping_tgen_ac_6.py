import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using tgen_ac_6.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:tgen_ac_6.obj=33bd88f67e335099f3ca78879fcf07466f44d313e44f90f5b404f380cc272a1d
    +test_classification:System
    +name: test_pcl5_pcl_arb_clipping_tgen_ac_6
    +test:
        +title: test_pcl5_pcl_arb_clipping_tgen_ac_6
        +guid:87d907ac-2168-419b-b84a-4fdb67bc616c
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_arb_clipping_tgen_ac_6(setup_teardown, printjob, outputsaver):
    printjob.print_verify('33bd88f67e335099f3ca78879fcf07466f44d313e44f90f5b404f380cc272a1d', timeout=600)
    outputsaver.save_output()
