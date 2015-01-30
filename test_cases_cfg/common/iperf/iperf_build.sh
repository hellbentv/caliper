build_iperf() {
        SrcPath=${BENCH_PATH}"420.iperf"
        MYPWD=${PWD}
        BuildPATH="$MYPWD/build.iperf"
        TOP_SRCDIR="$MYPWD/$SrcPath"
   myOBJPATH=${OBJPATH}/bin
   mkdir -p $BuildPATH

        if [ $ARCH = "x86_64" -o $ARCH = "x86_32" ]
        then
      pushd $BuildPATH
                $TOP_SRCDIR/configure
                make
                cp src/iperf ../$myOBJPATH/
      popd
      rm -rf $BuildPATH
        fi

        if [ $ARCH = "arm_64" -o $ARCH = "arm_32" ]
        then
      pushd $BuildPATH
                ac_cv_func_malloc_0_nonnull=yes $TOP_SRCDIR/configure #--host=$ARMCROSS
           make
           cp src/iperf ../$myOBJPATH/
      popd
      rm -rf $BuildPATH
        fi

        if [ $ARCH = "android" ]; then
            pushd $BuildPATH
            cp $TOP_SRCDIR/* ./ -rf
            cp include/config.android.h include/config.h
            cp include/iperf-int.android.h include/iperf-int.h
            ndk-build V=1 LOCAL_DISABLE_FORMAT_STRING_CHECKS=true
            cp ./libs/armeabi-v7a/iperf ../$myOBJPATH/
            popd
            rm -rf $BuildPATH
        fi
}

build_iperf
