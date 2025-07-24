import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 hpgl using pa.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:pa.obj=129950d89e0f499f6568795fac2f487febf794ee3899a4c51f15c87ff825749d
    +test_classification:System
    +name: test_pcl5_hpgl_vector_pa
    +test:
        +title: test_pcl5_hpgl_vector_pa
        +guid:9253f33a-428c-4fc0-9817-0f98372d5824
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_hpgl_vector_pa(setup_teardown, printjob, outputsaver):
    printjob.print_verify('129950d89e0f499f6568795fac2f487febf794ee3899a4c51f15c87ff825749d', timeout=600)
    outputsaver.save_output()
