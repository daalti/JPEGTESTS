import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using kdotcpv.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:720
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:kdotcpv.obj=c1e4f43488fa6eaaa15edb81085e077ab10f1b0aa93d7c5160139c76ca4a9604
    +test_classification:System
    +name: test_pcl5_pcl_fontdes_2bytetypeface_kdotcpv
    +test:
        +title: test_pcl5_pcl_fontdes_2bytetypeface_kdotcpv
        +guid:63091c2c-bfdf-447a-a489-e8e8291a3380
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_fontdes_2bytetypeface_kdotcpv(setup_teardown, printjob, outputsaver):
    printjob.print_verify('c1e4f43488fa6eaaa15edb81085e077ab10f1b0aa93d7c5160139c76ca4a9604', timeout=600)
    outputsaver.save_output()
