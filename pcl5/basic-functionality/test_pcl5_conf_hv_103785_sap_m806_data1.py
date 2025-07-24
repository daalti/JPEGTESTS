import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:PCL5 high value test using **103785-SAP-M806-data1.prn
    +test_tier: 1
    +is_manual:False
    +test_classification:System
    +reqid:DUNE-156300
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:103785-SAP-M806-data1.prn=9f800530a956d952e470869a61563daf98433d6469e158090d8bc3fbf67b6120
    +name:test_pcl5_conf_hv_103785_sap_m806_data1
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:PCL5
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_pcl5_conf_hv_103785_sap_m806_data1
        +guid:2cc13e95-184c-47be-8727-ada2edd1bd97
        +dut:
            +type:Simulator
            +configuration: DocumentFormat=PCL5

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_pcl5_conf_hv_103785_sap_m806_data1(setup_teardown, printjob, outputverifier):
    printjob.print_verify('9f800530a956d952e470869a61563daf98433d6469e158090d8bc3fbf67b6120')
    outputverifier.save_and_parse_output()
