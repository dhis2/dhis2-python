from typing import Optional
from pydantic import BaseModel


class DatabaseInfo(BaseModel):
    name: str
    user: str
    url: str
    databaseVersion: str
    spatialSupport: bool


class SystemInfo(BaseModel):
    contextPath: str
    userAgent: str
    calendar: str
    dateFormat: str
    serverDate: str
    lastAnalyticsTableSuccess: str
    intervalSinceLastAnalyticsTableSuccess: str
    lastAnalyticsTableRuntime: str
    lastSystemMonitoringSuccess: str
    version: str
    revision: str
    buildTime: str
    jasperReportsVersion: str
    environmentVariable: str
    environmentVariable: str
    readOnlyMode: Optional[str]
    nodeId: Optional[str]
    javaVersion: Optional[str]
    javaVendor: Optional[str]
    javaOpts: Optional[str]
    osName: Optional[str]
    osArchitecture: Optional[str]
    osVersion: Optional[str]
    externalDirectory: Optional[str]
    databaseInfo: Optional[DatabaseInfo]
    readReplicaCount: Optional[int]
    memoryInfo: Optional[str]
    cpuCores: Optional[int]
    encryption: bool
    emailConfigured: bool
    redisEnabled: bool
    systemId: str
    systemName: str
    instanceBaseUrl: str
    clusterHostname: str
    isMetadataVersionEnabled: bool
    isMetadataVersionEnabled: bool
