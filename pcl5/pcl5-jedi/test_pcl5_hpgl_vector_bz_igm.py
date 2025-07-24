import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 hpgl using bz_igm.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:720
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:bz_igm.obj=9da0ef52d0c958bac3804c758113178fa23c1987591d573bc9708fab47892833
    +test_classification:System
    +name: test_pcl5_hpgl_vector_bz_igm
    +test:
        +title: test_pcl5_hpgl_vector_bz_igm
        +guid:111570ed-16ac-4980-b9fa-f479ca127dfd
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_hpgl_vector_bz_igm(setup_teardown, printjob, outputsaver):
    printjob.print_verify('9da0ef52d0c958bac3804c758113178fa23c1987591d573bc9708fab47892833', timeout=600)
    outputsaver.save_output()
