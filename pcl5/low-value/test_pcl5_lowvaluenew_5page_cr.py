import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: pcl5 lowvaluenew using 5Page_cr.obj
    +test_tier: 3
    +is_manual: False
    +test_classification: 1
    +reqid: DUNE-37356
    +timeout:600
    +asset:PDL_Print
    +delivery_team:EnterpriseA4
    +feature_team:ENTA4ProductTest
    +test_framework: TUF
    +external_files:5Page-cr.obj=73154431b7c1648cd699874c2d4e80f79ce7153d575975ccaa4f17261f8e9326
    +test_classification:System
    +name: test_pcl5_lowvaluenew_5page_cr
    +test:
        +title: test_pcl5_lowvaluenew_5page_cr
        +guid:6236a95d-77a1-4a28-9198-ca16dba3d712
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_pcl5_lowvaluenew_5page_cr(setup_teardown, printjob, outputsaver):
    printjob.print_verify('73154431b7c1648cd699874c2d4e80f79ce7153d575975ccaa4f17261f8e9326', timeout=600)
    outputsaver.save_output()
