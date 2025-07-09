import pytest
import logging


"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose:Jpeg test using **Webpage_UPD_PRint.JPG
    +test_tier:1
    +is_manual:False
    +reqid:DUNE-17136
    +timeout:120
    +asset:PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework:TUF
    +external_files:Webpage_UPD_PRint.JPG=a89ef72d5101dabbf55a0722d57141626372518bfd7fa6b3ba53808ba7d1e0f5
    +test_classification:System
    +name:test_jpeg_webpage_upd_print
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:JPEG
        +interaction:Headless
        +test_type:Positive
    +test:
        +title:test_jpeg_webpage_upd_print
        +guid:9e272d3f-b05c-40e3-8d23-e78a519501bf
        +dut:
            +type:Simulator
            +configuration:DocumentFormat=JPEG

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_jpeg_webpage_upd_print(setup_teardown, printjob, outputsaver):
    printjob.print_verify('a89ef72d5101dabbf55a0722d57141626372518bfd7fa6b3ba53808ba7d1e0f5')
    outputsaver.save_output()
