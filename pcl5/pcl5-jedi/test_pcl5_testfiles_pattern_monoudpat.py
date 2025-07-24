import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 testfiles using monoUDPat.pcl
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:monoUDPat.pcl=76e5a1624c8d755fa860c9d967bb3b2f1984e28f719d0aa893321fc50a8f256f
    +test_classification:System
    +name: test_pcl5_testfiles_pattern_monoudpat
    +test:
        +title: test_pcl5_testfiles_pattern_monoudpat
        +guid:c484251b-7662-493b-9be9-f22678ae2595
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_testfiles_pattern_monoudpat(setup_teardown, printjob, outputsaver):
    printjob.print_verify('76e5a1624c8d755fa860c9d967bb3b2f1984e28f719d0aa893321fc50a8f256f', timeout=600)
    outputsaver.save_output()
