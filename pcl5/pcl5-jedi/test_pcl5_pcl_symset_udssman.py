import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using udssman.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:udssman.obj=ac89ff3b0353e637fe9641d536d5da70961b9bbf36c7ff3bf65128eeff67c5b2
    +test_classification:System
    +name: test_pcl5_pcl_symset_udssman
    +test:
        +title: test_pcl5_pcl_symset_udssman
        +guid:21ce4a24-9f87-48f2-9a68-179d4e1fa9af
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_symset_udssman(setup_teardown, printjob, outputsaver):
    printjob.print_verify('ac89ff3b0353e637fe9641d536d5da70961b9bbf36c7ff3bf65128eeff67c5b2', timeout=600)
    outputsaver.save_output()
