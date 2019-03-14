
"use strict";

let StartMotion = require('./StartMotion.js')
let CmdJointTrajectory = require('./CmdJointTrajectory.js')
let SetDrivePower = require('./SetDrivePower.js')
let SetRemoteLoggerLevel = require('./SetRemoteLoggerLevel.js')
let GetRobotInfo = require('./GetRobotInfo.js')
let StopMotion = require('./StopMotion.js')

module.exports = {
  StartMotion: StartMotion,
  CmdJointTrajectory: CmdJointTrajectory,
  SetDrivePower: SetDrivePower,
  SetRemoteLoggerLevel: SetRemoteLoggerLevel,
  GetRobotInfo: GetRobotInfo,
  StopMotion: StopMotion,
};
