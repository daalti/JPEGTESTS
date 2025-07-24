import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using ubpcleo.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:900
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:ubpcleo.obj=d96250d295b539bed365c0bc9eb5c57ead6e8f50218f1c8cb2bae97313f4926a
    +test_classification:System
    +name: test_pcl5_pcl_fontf_if_ubpcleo
    +test:
        +title: test_pcl5_pcl_fontf_if_ubpcleo
        +guid:9c37797d-c200-4dc3-aa26-b64b2c652658
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_fontf_if_ubpcleo(setup_teardown, printjob, outputsaver):
    printjob.print_verify('d96250d295b539bed365c0bc9eb5c57ead6e8f50218f1c8cb2bae97313f4926a', timeout=900)
    outputsaver.save_output()
