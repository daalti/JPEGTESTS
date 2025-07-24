import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 hpgl using pd_igm.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:pd_igm.obj=2747a936c4c1dd2ca35e983784ef5dba389eb5dc239867df3472e9e3f40555e1
    +test_classification:System
    +name: test_pcl5_hpgl_vector_pd_igm
    +test:
        +title: test_pcl5_hpgl_vector_pd_igm
        +guid:4a310d01-9061-48ec-a9f4-8111e4dbbb64
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_hpgl_vector_pd_igm(setup_teardown, printjob, outputsaver):
    printjob.print_verify('2747a936c4c1dd2ca35e983784ef5dba389eb5dc239867df3472e9e3f40555e1', timeout=600)
    outputsaver.save_output()
