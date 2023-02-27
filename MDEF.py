""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""" @file MDEF.py                                                                                                    """
""" Contains the definition of MDEF Class                                                                            """
""" Keep it sweetly simple                                                                                           """
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

import sys
from enum import Enum
from abc import abstractmethod
from collections import OrderedDict


class Constants(Enum):
    KEY = 'Key'
    NAME = 'Name'
    DATASOURCE = 'Datasource'
    BASEURL = 'BaseURL'
    PAGINATION = 'Pagination'
    PAGINATIONTYPE = 'PaginationType'
    MAXPAGESIZE = 'MaxPageSize'
    NEXTPAGEURL = 'NextPageURL'
    OFFSETISBYITEM = 'OffsetIsByItem'
    PAGESTARTINDEX = 'PageStartIndex'
    SVCREQPARAMOFFSET = 'SvcReqParam_Offset'
    SVCREQPARAMPAGESIZE = 'SvcReqParam_PageSize'
    SVCRESPATTRTERMINATIONELEMENT = 'SvcRespAttr_TerminationElement'
    SVCRESPATTRNEXTPAGEKEYELEMENT = 'SvcRespAttr_NextPageKeyElement'
    TESTURLENDPOINT = 'TestURL_endpoint'
    TIMESTAMPFORMAT = 'TimestampFormat'
    ISUNIXTIMESTAMPFORMAT = 'IsUnixTimeStampFormat'
    TIMESTAMPUNIT = 'TimestampUnit'
    ISLAZYINITIALIZATION = 'IsLazyInitialization'
    DOESSERVERSUPPORTTHROTTLING = 'DoesServerSupportThrottling'
    AUTHBROWSECONNECTMAP = 'AuthBrowseConnectMap'
    AUTHPROFILES = 'AuthProfiles'
    TABLENAME = 'TableName'
    TABLES = 'Tables'
    VIRTUALTABLES = 'VirtualTables'
    SKELETONTABLE = 'SkeletonTable'
    SKELETONCOLUMN = 'SkeletonColumn'
    TABLEDEFINITION = 'TableDefinition'
    COLUMNDEFINITION = 'ColumnDefinition'
    SORTABLE = 'Sortable'
    PAGEABLE = 'Pageable'
    COLUMNPUSHDOWN = 'ColumnPushdown'
    ITEMENDPOINTCOLUMNNAMES = 'ItemEndpointColumnNames'
    PKEYCOLUMN = 'PKeyColumn'
    FKEYCOLUMN = 'FKeyColumn'
    COLUMNS = 'Columns'
    APIACCESS = 'APIAccess'
    READAPI = 'ReadAPI'
    CREATEAPI = 'CreateAPI'
    UPDATEAPI = 'UpdateAPI'
    DELETEAPI = 'DeleteAPI'
    TABLESCHEMANAME = 'TableSchemaName'
    SUPPORT = 'Support'
    SVCREQPARAMKEY = 'SvcReqParam_Key'
    SVCREQPARAMDELIMITER = 'SvcReqParam_Delimiter'
    PKCOLUMNNAME = 'PKColumnName'
    RELATEDFKCOLUMNS = 'RelatedFKColumns'
    FOREIGNKEYCOLUMNS = 'ForeignKeyColumns'
    REFERENCETABLE = 'ReferenceTable'
    REFERENCETABLESCHEMA = 'ReferenceTableSchema'
    ISUNSIGNED = 'IsUnsigned'
    LENGTH = 'Length'
    PRECISION = 'Precision'
    SQLTYPE = 'SQLType'
    SCALE = 'Scale'
    SOURCETYPE = 'SourceType'
    METADATA = 'Metadata'
    COLUMNPUSHDOWN_MAPPING = 'ColumnPushdown_Mapping'
    NULLABLE = 'Nullable'
    PASSDOWNABLE = 'Passdownable'
    SVCREQPARAM_QUERYMAPPING = 'SvcReqParam_QueryMapping'
    SVCRESPATTR_ITEMRESULT = 'SvcRespAttr_ItemResult'
    SVCRESPATTR_LISTRESULT = 'SvcRespAttr_ListResult'
    SVCRESPATTR_RETURNIDPATH = 'SvcRespAttr_ReturnIdPath'
    SYNTHETICINDEXCOLUMN = 'SyntheticIndexColumn'
    PARENTCOLUMN = 'ParentColumn'
    UPDATABLE = 'Updatable'
    ISPARAMETER = 'IsParameter'
    ISREFERENCED = 'IsReferenced'
    MAXVALUESPERCALL = 'MaxValuesPerCall'
    SVCRESPATTRFIELD = 'SvcRespAttr_Field'
    KEYNAME = 'keyName'
    ROOT = 'Root'
    SVCREQPARAMKEYS = 'SvcReqParam_Keys'
    ITEMENDPOINT = 'ItemEndpoint'
    ITEMENDPOINTHASARRAYRESPONSE = 'ItemEndpointHasArrayResponse'
    LISTENDPOINT = 'ListEndpoint'
    PREREQCALL = 'PreReqCall'
    TYPE = 'Type'
    ACCEPT = 'Accept'
    BODYSKELETON = 'BodySkeleton'
    CONTENTTYPE = 'ContentType'
    DATAPATH = 'DataPath'
    ENDPOINT = 'Endpoint'
    ITEMROOT = 'ItemRoot'
    LISTROOT = 'ListRoot'
    METHOD = 'Method'
    COLUMNREQUIREMENTS = 'ColumnRequirements'
    PARAMETERFORMAT = 'ParameterFormat'
    ENCBROWSECONNECTKEY = 'EncBrowseConnectKey'
    ISSENSITIVEKEY = 'IsSensitiveKey'
    VALUE = 'Value'
    PATH = 'Path'
    HEADERS = 'Headers'
    EXPECTEDPARAMS = 'ExpectedParams'
    REQUIREDPARAMS = 'RequiredParams'
    SEQUENCE = 'Sequence'
    TOKENTYPE = 'TokenType'
    ISEXPIRATIONDATAAVAILABLE = 'IsExpirationDataAvailable'
    ISAUTOREFRESHSUPPORTED = 'IsAutoRefreshSupported'
    REFRESHTOKENWITHINRANGE = 'RefreshTokenWithinRange'
    AUTH_WINDOWHEIGHT = 'Auth_WindowHeight'
    AUTH_WINDOWWIDTH = 'Auth_WindowWidth'
    VERIFYHOST = 'VerifyHost'
    VERIFYPEER = 'VerifyPeer'
    LISTVARIABLESPRECALLS = 'ListVariablesPrecalls'
    LISTVARIABLEACCESS = 'ListVariableAccess'
    SVCRESPATTR_DEFAULTVALUE = 'SvcRespAttr_DefaultValue'
    SVCRESPATTR_MAPPING = 'SvcRespAttr_Mapping'
    ACCEPTTYPE = 'AcceptType'
    VARIABLES = 'Variables'
    VARIABLEROOT = 'VariableRoot'
    VARIABLENAME = 'VariableName'


class Parsable:
    """Represents Abstract Parsable class"""

    @abstractmethod
    def parse(self, inData):
        pass


class PrimaryKey:
    def __init__(self, inName: str, inFKCols: list[str]):
        self.__mRelatedFKColumns = inFKCols
        self.__mName = inName

    @property
    def Name(self):
        return self.__mName

    @property
    def RelatedFKColumns(self) -> list[str]:
        return self.__mRelatedFKColumns


class ForeignKeyColumn:

    def __init__(self, inForeignKey: str, inPrimaryKey: str):
        # Represents the column of the table as foreign key
        self.__mForeignKey = inForeignKey
        # Represents the column of the referenced table's primary key
        self.__mPrimaryKey = inPrimaryKey

    @property
    def ForeignKey(self):
        return self.__mForeignKey

    @ForeignKey.setter
    def ForeignKey(self, inForeignKey: str):
        self.__mForeignKey = inForeignKey

    @property
    def PrimaryKey(self):
        return self.__mPrimaryKey

    @PrimaryKey.setter
    def PrimaryKey(self, inPrimaryKey: str):
        self.__mPrimaryKey = inPrimaryKey


class ForeignKey(Parsable):
    def __init__(self):
        self.__mReferenceTableSchema = None
        self.__mReferenceTable = None
        self.__mForeignKeyColumns = list()

    def parse(self, inData):
        """Parses FKeyColumn MDEF Content"""
        assert isinstance(inData, dict)
        for key, val in inData.items():
            if Constants.FOREIGNKEYCOLUMNS.value == key:
                for fKey, pKey in val.items():
                    self.__mForeignKeyColumns.append(ForeignKeyColumn(fKey, pKey))
            elif Constants.REFERENCETABLE.value == key:
                self.__mReferenceTable = val
            elif Constants.REFERENCETABLESCHEMA.value == key:
                self.__mReferenceTableSchema = val
        return self

    @property
    def ForeignKeyColumns(self) -> list[ForeignKeyColumn]:
        return self.__mForeignKeyColumns

    @ForeignKeyColumns.setter
    def ForeignKeyColumns(self, inForeignKeyColumns: list[ForeignKeyColumn]):
        self.__mForeignKeyColumns = inForeignKeyColumns

    @property
    def ReferenceTable(self) -> str:
        return self.__mReferenceTable

    @ReferenceTable.setter
    def ReferenceTable(self, inReferenceTable: str):
        self.__mReferenceTable = inReferenceTable

    @property
    def ReferenceTableSchema(self) -> str:
        return self.__mReferenceTableSchema

    @ReferenceTableSchema.setter
    def ReferenceTableSchema(self, inReferenceTableSchema: str):
        self.__mReferenceTableSchema = inReferenceTableSchema


class ColumnMetadata(Parsable):
    def __init__(self):
        self.__mSourceType = ''
        self.__mScale = 0
        self.__mSQLType = None
        self.__mPrecision = 0
        self.__mLength = 0
        self.__mIsUnsigned = False

    def parse(self, inData):
        """Parses Column's Metadata content"""
        assert isinstance(inData, dict)
        for key, val in inData.items():
            if Constants.SQLTYPE.value == key:
                self.__mSQLType = val
            elif Constants.SOURCETYPE.value == key:
                self.__mSourceType = val
            elif Constants.LENGTH.value == key:
                self.__mLength = val
            elif Constants.PRECISION.value == key:
                self.__mPrecision = val
            elif Constants.SCALE.value == key:
                self.__mScale = val
            elif Constants.ISUNSIGNED.value == key:
                self.__mIsUnsigned = val
            else:
                raise Exception(f'Unhandled key encountered: {key}')
        return self

    @property
    def IsUnsigned(self) -> bool:
        return self.__mIsUnsigned

    @IsUnsigned.setter
    def IsUnsigned(self, isUnsigned: bool):
        self.__mIsUnsigned = isUnsigned

    @property
    def Length(self) -> int:
        return self.__mLength

    @Length.setter
    def Length(self, inLength: int):
        self.__mLength = inLength

    @property
    def Precision(self) -> int:
        return self.__mPrecision

    @Precision.setter
    def Precision(self, inPrecision: int):
        self.__mPrecision = inPrecision

    @property
    def Scale(self) -> int:
        return self.__mScale

    @Scale.setter
    def Scale(self, inScale: int):
        self.__mScale = inScale

    @property
    def SQLType(self) -> str:
        return self.__mSQLType

    @SQLType.setter
    def SQLType(self, inSQLType: str):
        self.__mSQLType = inSQLType

    @property
    def SourceType(self) -> str:
        return self.__mSourceType

    @SourceType.setter
    def SourceType(self, inSourceType: str):
        self.__mSourceType = inSourceType


class Column(Parsable):
    def __init__(self):
        self.__mParentColumn = None
        self.__mName = ''
        self.__mReturnIdPath = ''
        self.__mPushdownMapping = ''
        self.__mQueryMapping = ''
        self.__mItemResult = ''
        self.__mListResult = ''
        self.__mMetadata = None
        self.__mPassdownable = False
        self.__mUpdatable = False
        self.__mNullable = False
        self.__mSyntheticIndexColumn = False

    def parse(self, inData):
        """Parses Column MDEF Content"""
        assert isinstance(inData, dict)
        for key, val in inData.items():
            if Constants.NAME.value == key:
                self.__mName = val
            elif Constants.METADATA.value == key:
                self.__mMetadata = ColumnMetadata().parse(inData[Constants.METADATA.value])
            elif Constants.NULLABLE.value == key:
                self.__mNullable = val
            elif Constants.UPDATABLE.value == key:
                self.__mUpdatable = val
            elif Constants.PASSDOWNABLE.value == key:
                self.__mPassdownable = val
            elif Constants.SVCRESPATTR_LISTRESULT.value == key:
                self.__mListResult = val
            elif Constants.SVCRESPATTR_ITEMRESULT.value == key:
                self.__mItemResult = val
            elif Constants.SVCREQPARAM_QUERYMAPPING.value == key:
                self.__mQueryMapping = val
            elif Constants.SVCRESPATTR_RETURNIDPATH.value == key:
                self.__mReturnIdPath = val
            elif Constants.COLUMNPUSHDOWN_MAPPING.value == key:
                self.__mPushdownMapping = val
            elif Constants.SYNTHETICINDEXCOLUMN.value == key:
                self.__mSyntheticIndexColumn = val
            elif Constants.PARENTCOLUMN.value == key:
                self.__mParentColumn = int(val)
        return self

    @property
    def Name(self):
        return self.__mName

    @Name.setter
    def Name(self, inName: str):
        self.__mName = inName

    @property
    def SyntheticIndexColumn(self) -> bool:
        return self.__mSyntheticIndexColumn

    @SyntheticIndexColumn.setter
    def SyntheticIndexColumn(self, isSyntheticIndexColumn: bool):
        self.__mSyntheticIndexColumn = isSyntheticIndexColumn

    @property
    def Nullable(self) -> bool:
        return self.__mNullable

    @Nullable.setter
    def Nullable(self, isNullable: bool):
        self.__mNullable = isNullable

    @property
    def Updatable(self) -> bool:
        return self.__mUpdatable

    @Updatable.setter
    def Updatable(self, isUpdatable: bool):
        self.__mUpdatable = isUpdatable

    @property
    def Passdownable(self) -> bool:
        return self.__mPassdownable

    @Passdownable.setter
    def Passdownable(self, isPassdownable: bool):
        self.__mPassdownable = isPassdownable

    @property
    def Metadata(self) -> ColumnMetadata:
        return self.__mMetadata

    @Metadata.setter
    def Metadata(self, inMetadata: ColumnMetadata):
        self.__mMetadata = inMetadata

    @property
    def ListResult(self) -> str:
        return self.__mListResult

    @ListResult.setter
    def ListResult(self, inListResult: str):
        self.__mListResult = inListResult

    @property
    def ItemResult(self) -> str:
        return self.__mItemResult

    @ItemResult.setter
    def ItemResult(self, inItemResult: str):
        self.__mItemResult = inItemResult

    @property
    def QueryMapping(self) -> str:
        return self.__mQueryMapping

    @QueryMapping.setter
    def QueryMapping(self, inQueryMapping: str):
        self.__mQueryMapping = inQueryMapping

    @property
    def PushdownMapping(self) -> str:
        return self.__mPushdownMapping

    @PushdownMapping.setter
    def PushdownMapping(self, inPushdownMapping: str):
        self.__mPushdownMapping = inPushdownMapping

    @property
    def ReturnIdPath(self) -> str:
        return self.__mReturnIdPath

    @ReturnIdPath.setter
    def ReturnIdPath(self, inReturnIdPath: str):
        self.__mReturnIdPath = inReturnIdPath


class Table(Parsable):
    def __init__(self):
        self.__mVirtualTables = list()
        self.__mColumns = list()
        self.__mForeignKeys = list()
        self.__mPrimaryKeys = list()
        self.__mTableSchemaName = None
        self.__mItemEndpointColumnNames = list()
        self.__mName = None

    def parse(self, inData):
        """Parses Tables MDEF Content"""
        assert isinstance(inData, dict)
        for key, val in inData.items():
            if Constants.TABLENAME.value == key:
                self.__mName = val
            elif Constants.TABLESCHEMANAME.value == key:
                self.__mTableSchemaName = val
            elif Constants.ITEMENDPOINTCOLUMNNAMES.value == key:
                self.__mItemEndpointColumnNames = val
            elif Constants.COLUMNS.value == key:
                for colData in val:
                    column = Column().parse(colData)
                    self.__mColumns.append(column)
            elif Constants.FKEYCOLUMN.value == key:
                for item in val:
                    self.__mForeignKeys.append(ForeignKey().parse(item))
            elif Constants.VIRTUALTABLES.value == key:
                self.__mVirtualTables = VirtualTable(self.TableSchemaName, self.Name).parse(val)
            else:
                pass
                # raise Exception(f'Unhandled Key encountered: {key}')
        return self

    @property
    def Name(self) -> str:
        return self.__mName

    @Name.setter
    def Name(self, inName: str):
        self.__mName = inName

    @property
    def ItemEndpointColumnNames(self) -> list:
        return self.__mItemEndpointColumnNames

    @ItemEndpointColumnNames.setter
    def ItemEndpointColumnNames(self, inItemEndpointColumnNames: list[str]):
        self.__mItemEndpointColumnNames = inItemEndpointColumnNames

    @property
    def TableSchemaName(self) -> str:
        return self.__mTableSchemaName

    @TableSchemaName.setter
    def TableSchemaName(self, inTableSchemaName: str):
        self.__mTableSchemaName = inTableSchemaName

    @property
    def PrimaryKeys(self) -> list[PrimaryKey]:
        return self.__mPrimaryKeys

    @PrimaryKeys.setter
    def PrimaryKeys(self, inPrimaryKeys: list[PrimaryKey]):
        self.__mPrimaryKeys = inPrimaryKeys

    @property
    def ForeignKeys(self) -> list[ForeignKey]:
        return self.__mForeignKeys

    @ForeignKeys.setter
    def ForeignKeys(self, inForeignKey: list[ForeignKey]):
        self.__mForeignKeys = inForeignKey

    @property
    def Columns(self) -> list[Column]:
        return self.__mColumns

    @Columns.setter
    def Columns(self, inColumns: list[Column]):
        self.__mColumns = inColumns

    @property
    def VirtualTables(self) -> list:
        return self.__mVirtualTables

    @property
    def VirtualTableNames(self) -> list:
        vTableNames = list()
        for vTable in self.__mVirtualTables:
            vTableNames.append(vTable.FullName)
        return vTableNames

    @property
    def FullName(self):
        return f'{self.__mTableSchemaName}{MDEF.cleanName(self.__mName)}'


class VirtualTable(Table):
    def __init__(self, inSchema: str, inParentTable: str):
        super().__init__()
        self.TableSchemaName = inSchema
        self.__mParentTable = inParentTable

    def parse(self, inData):
        """Parses Virtual Table Data"""
        assert isinstance(inData, dict)
        virtualTables = list()
        for key, val in inData.items():
            if Constants.TABLENAME.value == key:
                self.Name = MDEF.cleanName(val)
            elif Constants.PKEYCOLUMN.value == key:
                for item in val.values():
                    assert isinstance(item, list)
                    for pKeyData in item:
                        self.PrimaryKeys.append(
                            PrimaryKey(
                                pKeyData[Constants.PKCOLUMNNAME.value],
                                pKeyData[Constants.RELATEDFKCOLUMNS.value]
                            )
                        )
            elif Constants.FKEYCOLUMN.value == key:
                assert isinstance(val, list)
                for item in val:
                    self.ForeignKeys.append(ForeignKey().parse(item))
            elif Constants.COLUMNS.value == key:
                assert isinstance(val, list)
                for item in val:
                    self.Columns.append(
                        Column().parse(item)
                    )
        if Constants.VIRTUALTABLES.value in inData:
            val = inData[Constants.VIRTUALTABLES.value]
            assert isinstance(val, list)
            for vTable in val:
                virtualTables.extend(VirtualTable(self.TableSchemaName, self.Name).parse(vTable))
        return virtualTables


class MDEF(Parsable):
    """Represents MDEF class"""

    def __init__(self):
        self.__mContent = None
        self.__mTables = list()
        self.__mParentTableNames = list()
        self.__mVirtualTableNames = list()
        self.__mVirtualTables = list()

    def parse(self, inMDEFContent: dict):
        """Parses the given MDEF content"""
        if inMDEFContent is None or len(inMDEFContent) == 0:
            print('Error: Empty MDEF Content to parse')
            sys.exit(1)

        self.__mContent = inMDEFContent
        self.__mTables = list()
        try:
            # Parse tables
            for tableData in self.__mContent[Constants.TABLES.value]:
                table = Table().parse(tableData)
                self.__mTables.append(table)
                self.__mParentTableNames.append(table.FullName)
                self.__mVirtualTables.extend(table.VirtualTables)
                self.__mVirtualTableNames.extend(table.VirtualTableNames)
        except KeyError as error:
            print(f'{error} key not found in MDEF')
            sys.exit(1)
        except Exception as error:
            print(f'Error: {error}')
            sys.exit(1)

    @property
    def Tables(self):
        return self.__mTables

    @property
    def TableNames(self) -> list[str]:
        return self.__mParentTableNames

    @property
    def VirtualTableNames(self) -> list[str]:
        return self.__mVirtualTableNames

    @property
    def AllTableNames(self) -> list:
        return self.__mParentTableNames + self.__mVirtualTableNames

    @staticmethod
    def cleanName(inName: str):
        """Removes Variable placeholders and separators"""
        inName = inName.replace('_', '')
        startIdx = inName.find('{{')
        if startIdx == -1:
            return inName
        else:
            endIdx = inName.find('}}')
            return f'{inName[:startIdx]}{inName[endIdx + 2:]}'

    def __sub__(self, inOtherInst):
        """
        Finds the difference of the MDEF configurations as an instance of MDEF
        :param inOtherInst: Another MDEF instance
        """
        if inOtherInst is None and not isinstance(inOtherInst, MDEF):
            print('Error: Empty/Corrupted MDEF Content provided')
            sys.exit(1)
        solicit = MDEF()
        # Finds new added tables
        solicit.TableNames.extend(set(self.TableNames).difference(inOtherInst.TableNames))
        for table in self.Tables:
            if table.FullName in solicit.TableNames:
                solicit.Tables.append(table)
                solicit.__mVirtualTableNames.extend(table.VirtualTableNames)
                solicit.__mVirtualTables.extend(table.VirtualTables)
        return solicit
