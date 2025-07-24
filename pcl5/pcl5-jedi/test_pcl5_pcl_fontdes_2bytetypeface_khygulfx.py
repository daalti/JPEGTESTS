import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 pcl using khygulfx.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:khygulfx.obj=c65c9446c1af8774ee661c9fc97dd41bd0fb2b45a60d69f4fd09cfa71197c9c9
    +test_classification:System
    +name: test_pcl5_pcl_fontdes_2bytetypeface_khygulfx
    +test:
        +title: test_pcl5_pcl_fontdes_2bytetypeface_khygulfx
        +guid:88cddad9-97a2-4d92-a4a2-9743921a0137
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_pcl_fontdes_2bytetypeface_khygulfx(setup_teardown, printjob, outputsaver):
    printjob.print_verify('c65c9446c1af8774ee661c9fc97dd41bd0fb2b45a60d69f4fd09cfa71197c9c9', timeout=600)
    outputsaver.save_output()
