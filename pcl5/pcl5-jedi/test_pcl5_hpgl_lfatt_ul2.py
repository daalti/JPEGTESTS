import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 hpgl using ul2.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:ul2.obj=54af8e9f5aa60bdc8095949ae04173813dc4779db00c5be8dedcc1a9c787aa0e
    +test_classification:System
    +name: test_pcl5_hpgl_lfatt_ul2
    +test:
        +title: test_pcl5_hpgl_lfatt_ul2
        +guid:4d079291-2887-4cd8-a951-679605520b2e
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_hpgl_lfatt_ul2(setup_teardown, printjob, outputsaver):
    printjob.print_verify('54af8e9f5aa60bdc8095949ae04173813dc4779db00c5be8dedcc1a9c787aa0e', timeout=600)
    outputsaver.save_output()
