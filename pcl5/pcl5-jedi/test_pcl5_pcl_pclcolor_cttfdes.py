import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using cttfdes.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:900
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:cttfdes.obj=a1c913c903ab81eb249816d9430d3ff586ed895d56bc2297f4b96ffddddfb45e
    +test_classification:System
    +name: test_pcl5_pcl_pclcolor_cttfdes
    +test:
        +title: test_pcl5_pcl_pclcolor_cttfdes
        +guid:673f563d-f6f9-4386-9d8b-7dd9a22ef2eb
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_pclcolor_cttfdes(setup_teardown, printjob, outputsaver):
    printjob.print_verify('a1c913c903ab81eb249816d9430d3ff586ed895d56bc2297f4b96ffddddfb45e', timeout=900)
    outputsaver.save_output()
