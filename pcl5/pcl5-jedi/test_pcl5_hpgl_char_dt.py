import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 hpgl using dt.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:dt.obj=ec4e7ce6336a0387ba022f655d168c115b3f605f7c28e1693e0547c0b16308d8
    +test_classification:System
    +name: test_pcl5_hpgl_char_dt
    +test:
        +title: test_pcl5_hpgl_char_dt
        +guid:0b7e3547-d28a-4c76-8245-c83cfdaabcfb
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_hpgl_char_dt(setup_teardown, printjob, outputsaver):
    printjob.print_verify('ec4e7ce6336a0387ba022f655d168c115b3f605f7c28e1693e0547c0b16308d8', timeout=600)
    outputsaver.save_output()
