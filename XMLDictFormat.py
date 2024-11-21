# This is not used and it just to show what the dictionary formats are like
# These can also be viewed as output jsons if that is toggled on.

Forward_Destinations_Dict = {
    "OfficeHoursDestination" : "## regex for DN='number'",
    "OutofOfficeHoursDestination" : "## regex for DN='number'",
    "HolidaysDestination" : "## regex for DN='number'"
}

DID_dict = {
    "Data" : "## Number of DID",
    "ForwardDistinations" : Forward_Destinations_Dict
}

Dict_of_DIDs = {
    "RuleName" : "Name of inbound did Rule",
    "DidNumbers" : "continious string of all DIDs",
    "ExternalNumber" : "Outbount caller ID",
    "RoutingRules" : DID_dict
}


IVR_Forward = {
    "Number" : "Number press to forward to location",
    "ForwardDN" : "## Location forwarded to",
    "ForwardType" : "Type of item forwarded to, IVR, queue etc"
}

#Tag for these items in this list is IVRForward
IVR_Forwards = {"ForwardDN": IVR_Forward}

IVR_Dict = {
    "Name" : "Name of IVR",
    "TimeoutForwardType": "Type of group when then call goes when it times out",
    "TimeoutForwardDN" : "## Location after a timeout",
    "Number" : "extensio of the IVR",
    "Forwards" : IVR_Forwards
}

Dict_of_IVRs = {"Number", IVR_Dict}


Queue_Destination = {
    "To" : "Destination Type",
    "Internal" : "DN=##"
}

member = {
    "Extension" : "## regex DN=",
    "Status" : "regex QueueStatus="
}

members = {
    "Extension" : member #This number will need to be grabbed via regex
}

Queue_managers = ["##regex for all DN="]

Queue_Dict = {
    "Name" : "Queue name",
    "Number" : "## Ext for the queue",
    "Destination" : Queue_Destination,
    "Members" : members,
    "QueueManagers" : Queue_managers
}

Dict_of_Queues = {
    "Number" : Queue_Dict
}

RingGroup_Dict = {
    "Number" : "Number of RG",
    "Destination" : "regex for DN=",
    "Members" : members,
    "Name" : "RG Name",
    "RingStrategy" : "Method for Ringing Members"
}

Dict_of_RingGroups = {
    "Number" : RingGroup_Dict
}

XML_Dictionary = {
    "IVRS" : Dict_of_IVRs,
    "DIDs" : Dict_of_DIDs,
    "Queues" : Dict_of_Queues,
    "RingGroup" : Dict_of_RingGroups
}

"""
Sampled DID

                <ExternalLine>
                    <AnswerAfter>0</AnswerAfter>
                    <DIDNumbers>555-123-4567, 555-123-4567, 555-123-4567, ...</DIDNumbers>
                    <Direction>Both</Direction>
                    <ExternalNumber>*555-123-4567</ExternalNumber>
                    <Gateway>Flowroute</Gateway>
                    <OutboundCallerID>555-123-4567</OutboundCallerID>
                    <RoutingRules>
                        <ExternalLineRule>
                            <Conditions>
                                <CallType Type="AllCalls" />
                                <Condition Type="BasedOnDID" />
                                <Hours Type="OfficeHours" />
                            </Conditions>
                            <Data>*15551234567</Data>
                            <ForwardDestinations>
                                <AlterDestinationDuringOutOfOfficeHours>True</AlterDestinationDuringOutOfOfficeHours>
                                <AlterDestinationDuringHolidays>False</AlterDestinationDuringHolidays>
                                <OfficeHoursDestination>
                                    <To>IVR</To>
                                    <Internal DN="8000" />
                                </OfficeHoursDestination>
                                <OutOfOfficeHoursDestination>
                                    <To>External</To>
                                    <External>12488585770</External>
                                    <Internal DN="8000" />
                                </OutOfOfficeHoursDestination>
                                <HolidaysDestination>
                                    <To>IVR</To>
                                    <Internal DN="HOL" />
                                </HolidaysDestination>
                            </ForwardDestinations>
                            <RuleName>Front Desk Main Line</RuleName>
                            <Hours HoursType="OfficeHours" IgnoreHolidays="False" />
                        </ExternalLineRule>
                    </RoutingRules>
                    </Properties>
                    <Hours HoursType="AllHours" IgnoreHolidays="False" />
"""

"""
Sampled IVR

<IVR>
    <Forwards>
        <IVRForward>
            <ForwardType>RingGroup</ForwardType>
            <Number>1</Number>
            <CustomData></CustomData>
            <ForwardDN>8101</ForwardDN>
        </IVRForward>
        <IVRForward>
            <ForwardType>Extension</ForwardType>
            <Number>2</Number>
            <CustomData></CustomData>
            <ForwardDN>2504</ForwardDN>
        </IVRForward>
        <IVRForward>
            <ForwardType>VoiceMail</ForwardType>
            <Number>3</Number>
            <CustomData></CustomData>
            <ForwardDN>7001</ForwardDN>
        </IVRForward>
    </Forwards>
    <Name>Main Reception IVR</Name>
    <PromptFilename>Promptrecording.wav</PromptFilename>
    <Timeout>60</Timeout>
    <TimeoutForwardDN>7001</TimeoutForwardDN>
    <TimeoutForwardType>VoiceMail</TimeoutForwardType>
    <UseMSExchange>False</UseMSExchange>
    <Number>8100</Number>
    <Hours HoursType="AllHours" IgnoreHolidays="False" />
</IVR>
"""

"""
Sample Call Queue

<Queue>
    <AnnouncementInterval>60</AnnouncementInterval>
    <AnnounceQueuePosition>False</AnnounceQueuePosition>
    <EnableIntro>True</EnableIntro>
    <Destination>
        <To>IVR</To>
        <Internal DN="8021" />
    </Destination>
    <IntroFile>Main Line -  Intro Prompt.wav</IntroFile>
    <MasterTimeout>120</MasterTimeout>
    <Name>Main Line Support</Name>
    <OnHoldFile>onhold.wav</OnHoldFile>
    <PollingStrategy>LongestWaiting</PollingStrategy>
    <Members>
        <Member DN="2506" QueueStatus="LoggedOut" SkillGroup="1" />
        <Member DN="2227" QueueStatus="LoggedIn" SkillGroup="1" />
        <Member DN="2168" QueueStatus="LoggedIn" SkillGroup="1" />
        <Member DN="1328" QueueStatus="LoggedOut" SkillGroup="1" />
    </Members>
    <QueueManagers>
        <Manager DN="1000" />
        <Manager DN="1538" />
        <Manager DN="2612" />
    </QueueManagers>
    <RingTimeout>20</RingTimeout>
    <Number>7153</Number>
    <Hours HoursType="AllHours" IgnoreHolidays="False" />
</Queue>
"""

"""
Sample RingGroup

<RingGroup>
    <Destination>
        <To>VoiceMail</To>
        <Internal DN="7001" />
    </Destination>
    <Members>
        <Member DN="2200" />
        <Member DN="2202" />
        <Member DN="2201" />
        <Member DN="2206" />
        <Member DN="2205" />
    </Members>
    <Name>Sales</Name>
    <RingStrategy>RingAll</RingStrategy>
    <RingTime>30</RingTime>
    <Number>8101</Number>
    <PhoneBookEntries />
    <Hours HoursType="AllHours" IgnoreHolidays="False" />
</RingGroup>
"""