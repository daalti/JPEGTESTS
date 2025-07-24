import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 hpgl using pe_igm.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:720
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:pe_igm.obj=d3f208a5e63c16bee42361255054139882a3428e960ee036e8eccdb236f7ae23
    +test_classification:System
    +name: test_pcl5_hpgl_vector_pe_igm
    +test:
        +title: test_pcl5_hpgl_vector_pe_igm
        +guid:4ba48c04-3295-400a-992c-45f3b04b24da
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_hpgl_vector_pe_igm(setup_teardown, printjob, outputsaver):
    printjob.print_verify('d3f208a5e63c16bee42361255054139882a3428e960ee036e8eccdb236f7ae23', timeout=600)
    outputsaver.save_output()
