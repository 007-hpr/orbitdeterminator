import numpy as np

def load_iod_data(fname):
    """ Loads satellite position observation data files following the Interactive
    Orbit Determination format (IOD). Currently, the only supported angle format
    are 1,2,3&7, as specified in IOD format.
    IOD format is described at http://www.satobs.org/position/IODformat.html.

    TODO: convert IOD angle formats 4,5&6 from AZ/EL to RA/DEC.

    Args:
        fname (string): name of the IOD-formatted text file to be parsed

    Returns:
        x (numpy array): array of satellite position observations following the
        IOD format, with angle format code = 2.
    """

    # dt is the dtype for IOD-formatted text files
    dt = 'S15, i8, S1,' \
         ' i8, i8, i8,' \
         ' i8, i8, i8, i8, i8, i8,' \
         ' i8, i8,' \
         ' S8, S7, i8, i8,' \
         ' S1, S1, i8, i8, i8'

    # iod_names correspond to the dtype names of each field
    iod_names = ['object', 'station', 'stationstatus',
                  'yr', 'month', 'day',
                  'hr', 'min', 'sec', 'msec', 'timeM', 'timeX',
                  'angformat', 'epoch',
                  'raaz', 'decel', 'radecazelM', 'radecazelX',
                  'optical', 'vismagsign', 'vismag', 'vismaguncertainty', 'flashperiod']

    # iod_delims corresponds to the delimiter for cutting the right variable from each input string
    iod_delims = [15, 5, 2,
                   5, 2, 2,
                   2, 2, 2, 3, 2, 1,
                   2, 1,
                   8, 7, 2, 1,
                   2, 1, 3, 3, 9]


    iod_input_lines = np.genfromtxt(fname, dtype=dt, names=iod_names, delimiter=iod_delims, autostrip=True)

    right_ascension = []
    declination = []
    azimuth = []
    elevation = []

    # work in progress. get_observations_data_sat() needs it still.
    # should be cleaned and centrally handled.
    raHH = []
    raMM = []
    rammm = []
    decDD = []
    decMM = []
    decmmm = []


    for i in range(len(iod_input_lines)):

        RAAZ = iod_input_lines["raaz"][i]
        raHH.append(RAAZ[0:3])
        raMM.append(RAAZ[3:5])
        rammm.append(RAAZ[5:7])
        RAAZ = RAAZ.decode()

        DECEL = iod_input_lines["decel"][i]
        decDD.append(DECEL[0:3])
        decMM.append(DECEL[3:5])
        decmmm.append(DECEL[5:7])
        DECEL = DECEL.decode()



        RA = -1.0
        DEC = -1.0
        AZ = -1.0
        EL = -1.0

        if iod_input_lines["angformat"][i] == 1:
            # 1: RA/DEC = HHMMSSs+DDMMSS MX   (MX in seconds of arc)
            HH = float(RAAZ[0:2])
            MM = float(RAAZ[2:4])
            SS = float(RAAZ[4:6])
            s = float(RAAZ[6])
            RA = (HH + (MM + (SS + s / 10.0) / 60.0) / 60.0) / 24.0 * 360.0

            DD = float(DECEL[1:3])
            MM = float(DECEL[3:5])
            SS = float(DECEL[5:7])
            DEC = DD + (MM + SS / 60.0) / 60.0
            if DECEL[0] == "-":
                DEC = -1.0 * DEC

        elif iod_input_lines["angformat"][i] == 2:
            # 2: RA/DEC = HHMMmmm+DDMMmm MX   (MX in minutes of arc)
            HH = float(RAAZ[0:2])
            MM = float(RAAZ[2:4])
            mmm = float(RAAZ[4:7])
            RA = (HH + (MM + mmm / 1000.0) / 60.0) / 24.0 * 360.0

            DD = float(DECEL[1:3])
            MM = float(DECEL[3:5])
            mm = float(DECEL[5:7])
            DEC = DD + (MM + mm / 100.0) / 60.0
            if DECEL[0] == "-":
                DEC = -1.0 * DEC

        elif iod_input_lines["angformat"][i] == 3:
            # 3: RA/DEC = HHMMmmm+DDdddd MX   (MX in degrees of arc)
            HH = float(RAAZ[0:2])
            MM = float(RAAZ[2:4])
            mmm = float(RAAZ[4:7])
            RA = (HH + (MM + mmm / 1000.0) / 60.0) / 24.0 * 360.0

            DD = float(DECEL[1:3])
            dddd = float(DECEL[3:7])
            DEC = (DD + (dddd / 1000.0))
            if DECEL[0] == "-":
                DEC = -1.0 * DEC

        elif iod_input_lines["angformat"][i] == 4:
            # 4: AZ/EL  = DDDMMSS+DDMMSS MX   (MX in seconds of arc)
            DDD = float(RAAZ[0:3])
            MM = float(RAAZ[3:5])
            SS = float(RAAZ[5:7])
            AZ = DDD + (MM + SS / 60.0) / 60.0

            DD = float(DECEL[1:3])
            MM = float(DECEL[3:5])
            SS = float(DECEL[5:7])
            EL = DD + (MM + SS / 60.0) / 60.0
            if DECEL[0] == "-":
                EL = -1.0 * EL

            # TODO: convert from AZ/EL to RA/DEC

        elif iod_input_lines["angformat"][i] == 5:
            # 5: AZ/EL  = DDDMMmm+DDMMmm MX   (MX in minutes of arc)
            DDD = float(RAAZ[0:3])
            MM = float(RAAZ[3:5])
            SS = float(RAAZ[5:7])
            AZ = DDD + (MM + SS / 60.0) / 60.0

            DD = float(DECEL[1:3])
            MM = float(DECEL[3:5])
            mm = float(DECEL[5:7])
            EL = DD + (MM + mm / 100.0) / 60.0
            if DECEL[0] == "-":
                EL = -1.0 * EL

            # TODO: convert from AZ/EL to RA/DEC

        elif iod_input_lines["angformat"][i] == 6:
            # 6: AZ/EL  = DDDdddd+DDdddd MX   (MX in degrees of arc)
            DDD = float(RAAZ[0:3])
            dddd = float(RAAZ[3:7])
            AZ = DDD + dddd / 1000.0

            DD = float(DECEL[1:3])
            dddd = float(DECEL[3:7])
            EL = DD + dddd / 1000.0
            if DECEL[0] == "-":
                EL = -1.0 * EL

            # TODO: convert from AZ/EL to RA/DEC

        elif iod_input_lines["angformat"][i] == 7:
            # 7: RA/DEC = HHMMSSs+DDdddd MX   (MX in degrees of arc)
            HH = float(RAAZ[0:2])
            MM = float(RAAZ[2:4])
            SS = float(RAAZ[4:6])
            s = float(RAAZ[6])
            RA = (HH + (MM + (SS + s / 10.0) / 60.0) / 60.0) / 24.0 * 360.0

            DD = float(DECEL[1:3])
            dddd = float(DECEL[3:7])
            DEC = (DD + (dddd / 1000.0))
            if DECEL[0] == "-":
                DEC = -1.0 * DEC

        #else:
        #    # TODO: when not defined, we assume it is RA/DEC

        right_ascension.append(RA)
        declination.append(DEC)
        azimuth.append(AZ)
        elevation.append(EL)

    # expanding the input iod data with the position data in different formats
    iod = {}
    for name in iod_names:
         iod[name] = iod_input_lines[name].tolist()

    iod["right_ascension"] = right_ascension
    iod["declination"] = declination
    iod["azimuth"] = azimuth
    iod["elevation"] = elevation

    iod["raHH"] = raHH
    iod["raMM"] = raMM
    iod["rammm"] = rammm

    iod["decDD"] = decDD
    iod["decMM"] = decMM
    iod["decmmm"] = decmmm

    return iod