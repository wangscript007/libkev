#!/usr/bin/python
#coding:utf-8
from __future__ import print_function
import sys
import os
import shutil

def get_sdkversion():
    output = os.popen('xcrun -sdk iphoneos --show-sdk-version')
    version = output.readline().strip('\n')
    output.close()
    return version

def get_xcode_root():
    output = os.popen('xcode-select -print-path')
    path = output.readline().strip('\n')
    output.close()
    return path

def run_and_check_error(command):
    if os.system(command) != 0:
        print('failed to execute: ', command)
        exit(-1)

def build_one_arch(workingPath, buildtype, arch, xcodePath):
    buildPath = workingPath + '/' + arch + '/' + buildtype
    if not os.path.exists(buildPath):
        os.makedirs(buildPath)
    os.chdir(buildPath)
    platform = 'iPhoneOS' if (arch == 'armv7' or arch == 'arm64') else 'iPhoneSimulator'
    os.environ['DEVROOT'] = '/'.join([xcodePath, 'Platforms', platform + '.platform', 'Developer'])
    os.environ['SDKROOT'] = os.environ['DEVROOT'] + '/SDKs/' + platform + '.sdk'
    os.environ['BUILD_TOOLS'] = xcodePath
    cmakeConfig = ['-DCMAKE_BUILD_TYPE='+buildtype,
                   '-DCMAKE_OSX_SYSROOT=$SDKROOT',
                   '-DCMAKE_SYSROOT=$SDKROOT',
                   '-DCMAKE_OSX_ARCHITECTURES='+arch,
                   '-DCMAKE_TARGET_SYSTEM=ios']
    run_and_check_error('cmake ../../../../.. ' + ' '.join(cmakeConfig))
    run_and_check_error('make')
    return buildPath+'/lib'

def build_ios(workingPath, outdir):
    xcodePath = get_xcode_root()

    os.system('rm -f '+outdir+'/Debug-iphoneos/libkev.a*')
    os.system('rm -f '+outdir+'/Release-iphoneos/libkev.a*')

    archs = ["armv7", "arm64", "x86_64"]
    arch = "armv7"
    build_one_arch(workingPath, 'Debug', arch, xcodePath)
    os.system('mv '+outdir+'/Debug-iphoneos/libkev.a '+outdir+'/Debug-iphoneos/libkev.a.'+arch)
    build_one_arch(workingPath, 'Release', arch, xcodePath)
    os.system('mv '+outdir+'/Release-iphoneos/libkev.a '+outdir+'/Release-iphoneos/libkev.a.'+arch)
    arch = "arm64"
    build_one_arch(workingPath, 'Debug', arch, xcodePath)
    os.system('mv '+outdir+'/Debug-iphoneos/libkev.a '+outdir+'/Debug-iphoneos/libkev.a.'+arch)
    build_one_arch(workingPath, 'Release', arch, xcodePath)
    os.system('mv '+outdir+'/Release-iphoneos/libkev.a '+outdir+'/Release-iphoneos/libkev.a.'+arch)
    os.system('lipo -create '+outdir+'/Debug-iphoneos/libkev.a.armv7 '+outdir+'/Debug-iphoneos/libkev.a.arm64 -output '+outdir+'/Debug-iphoneos/libkev.a')
    os.system('lipo -create '+outdir+'/Release-iphoneos/libkev.a.armv7 '+outdir+'/Release-iphoneos/libkev.a.arm64 -output '+outdir+'/Release-iphoneos/libkev.a')
    os.system('rm -f '+outdir+'/Debug-iphoneos/libkev.a.*')
    os.system('rm -f '+outdir+'/Release-iphoneos/libkev.a.*')

    arch = "x86_64"
    build_one_arch(workingPath, 'Debug', arch, xcodePath)
    build_one_arch(workingPath, 'Release', arch, xcodePath)


def ios_main(argv):
    workingPath = os.path.split(os.path.realpath(__file__))[0] + '/out'
    if not os.path.exists(workingPath):
        os.makedirs(workingPath)
    os.chdir(workingPath)
    outdir = workingPath + '/../../../lib/ios'
    build_ios(workingPath, outdir)

if __name__ == '__main__':
    ios_main(sys.argv)
