import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 hpgl using pg.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:pg.obj=69546298d0012177f1d1584d8ccf07ec5ce5760657f3afeb3f6057d059e3bd80
    +test_classification:System
    +name: test_pcl5_hpgl_cfgstat_pg
    +test:
        +title: test_pcl5_hpgl_cfgstat_pg
        +guid:5e40e308-4901-4432-ab9a-6e97f20dd5e4
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_hpgl_cfgstat_pg(setup_teardown, printjob, outputsaver):
    printjob.print_verify('69546298d0012177f1d1584d8ccf07ec5ce5760657f3afeb3f6057d059e3bd80', timeout=600)
    outputsaver.save_output()
