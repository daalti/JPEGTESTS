import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using pfancpt2.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:900
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:pfancpt2.obj=b037cb5685378216d9cefaba859315cc43e55a15436f99789bab333b5a66af7d
    +test_classification:System
    +name: test_pcl5_pcl_pcl_hpgl_pfancpt2
    +test:
        +title: test_pcl5_pcl_pcl_hpgl_pfancpt2
        +guid:1e4feafb-d4c2-4da6-a762-82231d5a1d1e
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_pcl_hpgl_pfancpt2(setup_teardown, printjob, outputsaver):
    printjob.print_verify('b037cb5685378216d9cefaba859315cc43e55a15436f99789bab333b5a66af7d', timeout=900)
    outputsaver.save_output()
