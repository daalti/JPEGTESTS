import os
import time
import logging
import pytest
import subprocess
from dunetuf.scp import SCP
from dunetuf.engine.maia.Utils import Utils


PRINTER_LOG_TEST_PATH =     "/tmp/printer.log"
PRINTER_LOG_PREV_TEST_PATH =     "/tmp/printer_prev.log"
PRINTER_LOG_PRINTER_PATH =  "/pe/zynq0/rootfs/data/log/printer.log"
PRINTER_LOG_PRINTER_PATTERN =  "/pe/zynq0/rootfs/data/log/printer.*"
# Tailgating Termination Trace.
TAIL_GATING_END_MSSG = ["INFO: internalTerminateRaster: FORCED raster terminated, breaking configured tailgating: doing termination"]
# Tailgating no termination Trace. 
TAIL_GATING_NO_TERMINATE_MSSG = ["INFO: internalTerminateRaster: raster terminated, in tailgating, not doing termination (no termination requested)"]


MAX_TG_NO_TERMINATE_MSSG        = 1 
MAX_TG_END_MSSG                 = 1 

JOB_PAGES_NUMBER = 3
MAX_TG_MULTIPAGE_NO_TERM_MSSG   = JOB_PAGES_NUMBER
MAX_TG_MULTIPAGE_END_MSSG       = 1 

MAX_TG_MULTIPAGE_DIFFERENT_CRC_NO_TERM_MSSG = MAX_TG_MULTIPAGE_NO_TERM_MSSG + 1
MAX_TG_MULTIPAGE_DIFFERENT_CRC_END_MSSG       = 2

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Simple print from a rasterstream (.rs) file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid: DUNE-52149
    +timeout:220
    +asset: PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:a3.rs=b53558fc131816862dde6ac63bbb30da4cad7c914906e050348a9bb09b629617
    +name: test_rs_a3_singlePage_tailgating
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:RasterStream
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_rs_a3_singlePage_tailgating
        +guid:b2bb5708-3e51-11ec-b54c-4fb3809df121
        +dut:
            +type: Emulator
            +configuration: DocumentFormat=RasterStreamICF

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""

def test_rs_a3_singlePage_tailgating(setup_teardown,spice, printjob, outputsaver, net, scp,job):

    global MAX_TG_NO_TERMINATE_MSSG
    global MAX_TG_END_MSSG
    spice.cleanSystemEventAndWaitHomeScreen()
    job.wait_for_no_active_jobs()
    # Downloads Printer.log
    _scp_download(net, scp)
    resp = check_printer_log(PRINTER_LOG_TEST_PATH)
    no_ter_mssg =  resp['no_terminate_mssg'] 
    end_mssg   =  resp['end_tailgating_mssg'] 
    print("No Terminate Message : {0}".format(no_ter_mssg))
    print("End Message : {0}".format(end_mssg))
    # Prints Single Page
    printjob.print_verify('b53558fc131816862dde6ac63bbb30da4cad7c914906e050348a9bb09b629617', timeout = 160)
    outputsaver.save_output()
    time.sleep(20)
    _scp_download(net, scp)
    resp = check_printer_log(PRINTER_LOG_TEST_PATH)
    print("No Terminate Message : {0}".format(resp['no_terminate_mssg']))
    print("End Message : {0}".format(resp['end_tailgating_mssg']))
    assert (resp['no_terminate_mssg'] - no_ter_mssg)  == MAX_TG_NO_TERMINATE_MSSG
    assert (resp['end_tailgating_mssg'] - end_mssg)  == MAX_TG_END_MSSG

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Multipage print from a rasterstream (.rs) file
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid: DUNE-52149
    +timeout:500
    +asset: PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:tower_a1_3pages.rs=ddf0ad85e52843dad222cbfebb28df8e748781b7b265ce1b7e1e834b6f890689
    +name: test_rs_a1_multipage_tailgating
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:RasterStream
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_rs_a1_multipage_tailgating
        +guid:638287a2-3e19-11ec-b8bc-a762c6009bcf
        +dut:
            +type: Emulator
            +configuration: DocumentFormat=RasterStreamICF

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
@pytest.mark.timeout(500)
def test_rs_a1_multipage_tailgating(setup_teardown, printjob, outputsaver, net, scp, tcl,job,ssh):

    global MAX_TG_MULTIPAGE_NO_TERM_MSSG
    global MAX_TG_MULTIPAGE_END_MSSG

    job.wait_for_no_active_jobs()
    #Downloads Printer.log
    _scp_download(net, scp)
    resp = check_printer_log(PRINTER_LOG_TEST_PATH)
    no_ter_mssg =  resp['no_terminate_mssg'] 
    end_mssg   =  resp['end_tailgating_mssg']
    print("No Terminate Message : {0}".format(no_ter_mssg))
    print("End Message : {0}".format(end_mssg))
    # Prints Multipage Job(3 pages)
    printjob.print_verify('ddf0ad85e52843dad222cbfebb28df8e748781b7b265ce1b7e1e834b6f890689', timeout=900)
    outputsaver.save_output()
    time.sleep(30)
    _scp_download(net, scp)
    resp = check_printer_log(PRINTER_LOG_TEST_PATH)
    print("No Terminate Tailgating Messages : {0}".format(resp['no_terminate_mssg']))
    print("End Tailgating Messages : {0}".format(resp['end_tailgating_mssg']))

    after_no_ter_mssg = 0
    after_end_mssg = 0
    
    if  resp['no_terminate_mssg'] < no_ter_mssg:
        after_no_ter_mssg = resp['no_terminate_mssg']
        after_end_mssg   =  resp['end_tailgating_mssg']
        print("Printer log truncated in the middle of the test : evaluate previous truncated")
        _scp_download_prev(net,scp,ssh)
        resp = check_printer_log(PRINTER_LOG_PREV_TEST_PATH)
        print("No Terminate Tailgating Messages prev: {0}".format(resp['no_terminate_mssg']))
        print("End Message  prev: {0}".format(resp['end_tailgating_mssg']))
    
    assert (resp['no_terminate_mssg'] +  after_no_ter_mssg - no_ter_mssg)  == MAX_TG_MULTIPAGE_NO_TERM_MSSG
    assert (resp['end_tailgating_mssg'] + after_end_mssg - end_mssg)  == MAX_TG_END_MSSG

"""
$$$$$_BEGIN_TEST_METADATA_DECLARATION_$$$$$
    +purpose: Multipage print from a rasterstream (.rs) file with crc
    +test_tier:1
    +is_manual:False
    +test_classification:System
    +reqid: DUNE-232825
    +timeout:350
    +asset: PDL_Print
    +delivery_team:PDLJobPQ
    +feature_team:PDLSolns
    +test_framework: TUF
    +external_files:tower_a1_3pages.rs=ddf0ad85e52843dad222cbfebb28df8e748781b7b265ce1b7e1e834b6f890689&lenna_100_dpi.jpg=7a2e13bafa3b09a94ae8a5c92592c36f3104d8eb862dd121f505fd11262fc242
    +name: test_rs_a1_multipage_with_different_crc_tailgating
    +categorization:
        +segment:Platform
        +area:Print
        +feature:PDL
        +sub_feature:RasterStream
        +interaction:Headless
        +test_type:Positive
    +test:
        +title: test_rs_a1_multipage_with_different_crc_tailgating
        +guid:5d1d7454-b5cb-4298-96a3-04b5165461fc
        +dut:
            +type: Emulator
            +configuration: DocumentFormat=RasterStreamICF

$$$$$_END_TEST_METADATA_DECLARATION_$$$$$
"""
def test_rs_a1_multipage_with_different_crc_tailgating(setup_teardown, printjob, outputsaver, net, scp, tcl,job):

    # Engine PageDataBase has 5 pages. So after using the 5 pages one of them will be reused
    global MAX_TG_MULTIPAGE_DIFFERENT_CRC_NO_TERM_MSSG
    global MAX_TG_MULTIPAGE_DIFFERENT_CRC_END_MSSG

    job.wait_for_no_active_jobs()
    #Downloads Printer.log
    _scp_download(net, scp)
    resp = check_printer_log(PRINTER_LOG_TEST_PATH)
    no_ter_mssg =  resp['no_terminate_mssg'] 
    end_mssg   =  resp['end_tailgating_mssg']
    print("No Terminate Message : {0}".format(no_ter_mssg))
    print("End Message : {0}".format(end_mssg))
    #Print job with colormap crc
    outputsaver.operation_mode('TIFF')
    printjob.send_file('7a2e13bafa3b09a94ae8a5c92592c36f3104d8eb862dd121f505fd11262fc242')  # has crc
    outputsaver.operation_mode('NONE')
    # Prints Multipage Job(3 pages) again. So the second page will reuse page of PageDatabase
    printjob.print_verify('ddf0ad85e52843dad222cbfebb28df8e748781b7b265ce1b7e1e834b6f890689', timeout=300)  # no crc
    outputsaver.save_output()
    _scp_download(net, scp)
    resp = check_printer_log(PRINTER_LOG_TEST_PATH)

    print("No Terminate Tailgating Messages : {0}".format(resp['no_terminate_mssg']))
    print("End Tailgating Messages : {0}".format(resp['end_tailgating_mssg']))

    after_no_ter_mssg = 0
    after_end_mssg = 0
    
    if  resp['no_terminate_mssg'] < no_ter_mssg:
        after_no_ter_mssg = resp['no_terminate_mssg']
        after_end_mssg   =  resp['end_tailgating_mssg']
        print("Printer log truncated in the middle of the test : evaluate previous truncated")
        _scp_download_prev(net,scp,ssh)
        resp = check_printer_log(PRINTER_LOG_PREV_TEST_PATH)
        print("No Terminate Tailgating Messages prev: {0}".format(resp['no_terminate_mssg']))
        print("End Message  prev: {0}".format(resp['end_tailgating_mssg']))
    
    
    #Verify that tailgating has not been brocken
    assert (resp['no_terminate_mssg'] +  after_no_ter_mssg - no_ter_mssg)  == MAX_TG_MULTIPAGE_DIFFERENT_CRC_NO_TERM_MSSG
    assert (resp['end_tailgating_mssg'] + after_end_mssg - end_mssg)  == MAX_TG_MULTIPAGE_DIFFERENT_CRC_END_MSSG

def check_printer_log(file_path): 
    
    """
        Checks Tailgating Traces in Printer Log Output.
    """

    tail_gating_trace_record = dict(no_terminate_mssg = 0, end_tailgating_mssg = 0)
    #printer_log = open(PRINTER_LOG_TEST_PATH, "r")
    printer_log = open(file_path, 'r+', encoding="ISO-8859-1")
    print("check_printer_log : {0}".format(file_path))
    try:
        found = 0
        index = 0
        no_ter_mssg = 0
        end_mssg_cont = 0
        line = ''
        for line in printer_log:  
            index += 1 
            # checking tailgating strings are present
            if TAIL_GATING_NO_TERMINATE_MSSG[0] in line:
                no_ter_mssg += 1
                print("Found TAIL_GATING_NO_TERMINATE_MSSG - Line {0}".format(index))
                found  = 1
            elif TAIL_GATING_END_MSSG[0] in line: 
                end_mssg_cont += 1
                print("Found TAIL_GATING_END_MSSG - Line : {0}".format(index))
            else :
                pass
    finally: 
        printer_log.close()
    if found == 1: 
        print("Found Tailgating Traces")
    else: 
        print("No tailgating traces found")

    print("Printer Log Lines : {0}".format(index))
    tail_gating_trace_record['no_terminate_mssg']   = no_ter_mssg
    tail_gating_trace_record['end_tailgating_mssg'] = end_mssg_cont
    print("check_printer_log no_terminate_mssg : {0}".format(no_ter_mssg))
    print("check_printer_log end_tailgating_mssg : {0}".format(end_mssg_cont))

    return tail_gating_trace_record

def _scp_download(net, scp): 
    """
      SCP File Transfer to PE Maia
    """
    global PRINTER_LOG_TEST_PATH
    global PRINTER_LOG_PRINTER_PATH
    dest    =  PRINTER_LOG_TEST_PATH
    source  =  PRINTER_LOG_PRINTER_PATH

    utils_maia = Utils(scp, net)
    utils_maia.download(source, dest)

def _scp_download_prev(net, scp,ssh): 
    """
      SCP File Transfer to PE Maia
    """
    global PRINTER_LOG_PREV_TEST_PATH
    global PRINTER_LOG_PRINTER_PATTERN

    dest    =  PRINTER_LOG_PREV_TEST_PATH
    comando = "ls -tr " + PRINTER_LOG_PRINTER_PATTERN + " | tail -n 2 | head -n 1"
    print("comando: {0}".format(comando))
    prev_log_file = ssh.run(comando)
    source = prev_log_file[:-4]
    #source = prev_log_file.removesuffix('.gz')
    print("Archivo a evaluar: {0}".format(source))

    utils_maia = Utils(scp, net)
    utils_maia.download(source, dest)
