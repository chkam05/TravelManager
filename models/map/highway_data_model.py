from __future__ import annotations
from dataclasses import dataclass
from typing import Any, ClassVar, Dict

from core.data.base_data_model import BaseDataModel


@dataclass
class HighwayDataModel(BaseDataModel):
    """Stores OpenStreetMap tag values defined by OpenStreetMap PrimaryFeaturesAttr.HighwayAttr."""

    # Default values
    _DEFAULT_VALUE: ClassVar[Any] = None

    # Field name declarations
    FIELD_ABUTTERS: ClassVar[str] = 'abutters'
    FIELD_BICYCLE_ROAD: ClassVar[str] = 'bicycle_road'
    FIELD_BUS_BAY: ClassVar[str] = 'bus_bay'
    FIELD_CHANGE: ClassVar[str] = 'change'
    FIELD_DESTINATION: ClassVar[str] = 'destination'
    FIELD_EMBANKMENT: ClassVar[str] = 'embankment'
    FIELD_EMBEDDED_RAILS: ClassVar[str] = 'embedded_rails'
    FIELD_FORD: ClassVar[str] = 'ford'
    FIELD_FRONTAGE_ROAD: ClassVar[str] = 'frontage_road'
    FIELD_ICE_ROAD: ClassVar[str] = 'ice_road'
    FIELD_INCLINE: ClassVar[str] = 'incline'
    FIELD_JUNCTION: ClassVar[str] = 'junction'
    FIELD_LANES: ClassVar[str] = 'lanes'
    FIELD_LANE_MARKINGS: ClassVar[str] = 'lane_markings'
    FIELD_LIT: ClassVar[str] = 'lit'
    FIELD_MAXSPEED: ClassVar[str] = 'maxspeed'
    FIELD_MOTORROAD: ClassVar[str] = 'motorroad'
    FIELD_MOUNTAIN_PASS: ClassVar[str] = 'mountain_pass'
    FIELD_MTB_SCALE: ClassVar[str] = 'mtb_scale'
    FIELD_MTB_SCALE_UPHILL: ClassVar[str] = 'mtb_scale_uphill'
    FIELD_MTB_SCALE_IMBA: ClassVar[str] = 'mtb_scale_imba'
    FIELD_MTB_DESCRIPTION: ClassVar[str] = 'mtb_description'
    FIELD_ONEWAY: ClassVar[str] = 'oneway'
    FIELD_ONEWAY_BICYCLE: ClassVar[str] = 'oneway_bicycle'
    FIELD_OVERTAKING: ClassVar[str] = 'overtaking'
    FIELD_PARKING_LANE: ClassVar[str] = 'parking_lane'
    FIELD_PARKING_CONDITION: ClassVar[str] = 'parking_condition'
    FIELD_PASSING_PLACES: ClassVar[str] = 'passing_places'
    FIELD_PRIORITY: ClassVar[str] = 'priority'
    FIELD_PRIORITY_ROAD: ClassVar[str] = 'priority_road'
    FIELD_SAC_SCALE: ClassVar[str] = 'sac_scale'
    FIELD_SERVICE: ClassVar[str] = 'service'
    FIELD_SHOULDER: ClassVar[str] = 'shoulder'
    FIELD_SIDE_ROAD: ClassVar[str] = 'side_road'
    FIELD_SMOOTHNESS: ClassVar[str] = 'smoothness'
    FIELD_SURFACE: ClassVar[str] = 'surface'
    FIELD_TACTILE_PAVING: ClassVar[str] = 'tactile_paving'
    FIELD_TRACKTYPE: ClassVar[str] = 'tracktype'
    FIELD_TRAFFIC_CALMING: ClassVar[str] = 'traffic_calming'
    FIELD_TRAIL_VISIBILITY: ClassVar[str] = 'trail_visibility'
    FIELD_TRAILBLAZED: ClassVar[str] = 'trailblazed'
    FIELD_TRAILBLAZED_VISIBILITY: ClassVar[str] = 'trailblazed_visibility'
    FIELD_TURN: ClassVar[str] = 'turn'
    FIELD_WIDTH: ClassVar[str] = 'width'
    FIELD_WINTER_ROAD: ClassVar[str] = 'winter_road'

    # OpenStreetMap tag declarations
    TAG_ABUTTERS: ClassVar[str] = 'abutters'
    TAG_BICYCLE_ROAD: ClassVar[str] = 'bicycle_road'
    TAG_BUS_BAY: ClassVar[str] = 'bus_bay'
    TAG_CHANGE: ClassVar[str] = 'change'
    TAG_DESTINATION: ClassVar[str] = 'destination'
    TAG_EMBANKMENT: ClassVar[str] = 'embankment'
    TAG_EMBEDDED_RAILS: ClassVar[str] = 'embedded_rails'
    TAG_FORD: ClassVar[str] = 'ford'
    TAG_FRONTAGE_ROAD: ClassVar[str] = 'frontage_road'
    TAG_ICE_ROAD: ClassVar[str] = 'ice_road'
    TAG_INCLINE: ClassVar[str] = 'incline'
    TAG_JUNCTION: ClassVar[str] = 'junction'
    TAG_LANES: ClassVar[str] = 'lanes'
    TAG_LANE_MARKINGS: ClassVar[str] = 'lane_markings'
    TAG_LIT: ClassVar[str] = 'lit'
    TAG_MAXSPEED: ClassVar[str] = 'maxspeed'
    TAG_MOTORROAD: ClassVar[str] = 'motorroad'
    TAG_MOUNTAIN_PASS: ClassVar[str] = 'mountain_pass'
    TAG_MTB_SCALE: ClassVar[str] = 'mtb:scale'
    TAG_MTB_SCALE_UPHILL: ClassVar[str] = 'mtb:scale:uphill'
    TAG_MTB_SCALE_IMBA: ClassVar[str] = 'mtb:scale:imba'
    TAG_MTB_DESCRIPTION: ClassVar[str] = 'mtb:description'
    TAG_ONEWAY: ClassVar[str] = 'oneway'
    TAG_ONEWAY_BICYCLE: ClassVar[str] = 'oneway:bicycle'
    TAG_OVERTAKING: ClassVar[str] = 'overtaking'
    TAG_PARKING_LANE: ClassVar[str] = 'parking:lane'
    TAG_PARKING_CONDITION: ClassVar[str] = 'parking:condition'
    TAG_PASSING_PLACES: ClassVar[str] = 'passing_places'
    TAG_PRIORITY: ClassVar[str] = 'priority'
    TAG_PRIORITY_ROAD: ClassVar[str] = 'priority_road'
    TAG_SAC_SCALE: ClassVar[str] = 'sac_scale'
    TAG_SERVICE: ClassVar[str] = 'service'
    TAG_SHOULDER: ClassVar[str] = 'shoulder'
    TAG_SIDE_ROAD: ClassVar[str] = 'side_road'
    TAG_SMOOTHNESS: ClassVar[str] = 'smoothness'
    TAG_SURFACE: ClassVar[str] = 'surface'
    TAG_TACTILE_PAVING: ClassVar[str] = 'tactile_paving'
    TAG_TRACKTYPE: ClassVar[str] = 'tracktype'
    TAG_TRAFFIC_CALMING: ClassVar[str] = 'traffic_calming'
    TAG_TRAIL_VISIBILITY: ClassVar[str] = 'trail_visibility'
    TAG_TRAILBLAZED: ClassVar[str] = 'trailblazed'
    TAG_TRAILBLAZED_VISIBILITY: ClassVar[str] = 'trailblazed:visibility'
    TAG_TURN: ClassVar[str] = 'turn'
    TAG_WIDTH: ClassVar[str] = 'width'
    TAG_WINTER_ROAD: ClassVar[str] = 'winter_road'

    # Fields
    abutters: Any | None
    bicycle_road: Any | None
    bus_bay: Any | None
    change: Any | None
    destination: Any | None
    embankment: Any | None
    embedded_rails: Any | None
    ford: Any | None
    frontage_road: Any | None
    ice_road: Any | None
    incline: Any | None
    junction: Any | None
    lanes: Any | None
    lane_markings: Any | None
    lit: Any | None
    maxspeed: Any | None
    motorroad: Any | None
    mountain_pass: Any | None
    mtb_scale: Any | None
    mtb_scale_uphill: Any | None
    mtb_scale_imba: Any | None
    mtb_description: Any | None
    oneway: Any | None
    oneway_bicycle: Any | None
    overtaking: Any | None
    parking_lane: Any | None
    parking_condition: Any | None
    passing_places: Any | None
    priority: Any | None
    priority_road: Any | None
    sac_scale: Any | None
    service: Any | None
    shoulder: Any | None
    side_road: Any | None
    smoothness: Any | None
    surface: Any | None
    tactile_paving: Any | None
    tracktype: Any | None
    traffic_calming: Any | None
    trail_visibility: Any | None
    trailblazed: Any | None
    trailblazed_visibility: Any | None
    turn: Any | None
    width: Any | None
    winter_road: Any | None

    #region Serialization

    @classmethod
    def _get_value(cls, d: Dict[str, Any], field_name: str, tag_name: str) -> Any:
        """Gets a value by local field name or by the real OpenStreetMap tag key."""
        return d.get(tag_name, d.get(field_name, cls._DEFAULT_VALUE))

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> HighwayDataModel:
        """Deserializes data from a dictionary in "attribute:value" format to an object."""
        return cls(
            abutters=cls._get_value(d, cls.FIELD_ABUTTERS, cls.TAG_ABUTTERS),
            bicycle_road=cls._get_value(d, cls.FIELD_BICYCLE_ROAD, cls.TAG_BICYCLE_ROAD),
            bus_bay=cls._get_value(d, cls.FIELD_BUS_BAY, cls.TAG_BUS_BAY),
            change=cls._get_value(d, cls.FIELD_CHANGE, cls.TAG_CHANGE),
            destination=cls._get_value(d, cls.FIELD_DESTINATION, cls.TAG_DESTINATION),
            embankment=cls._get_value(d, cls.FIELD_EMBANKMENT, cls.TAG_EMBANKMENT),
            embedded_rails=cls._get_value(d, cls.FIELD_EMBEDDED_RAILS, cls.TAG_EMBEDDED_RAILS),
            ford=cls._get_value(d, cls.FIELD_FORD, cls.TAG_FORD),
            frontage_road=cls._get_value(d, cls.FIELD_FRONTAGE_ROAD, cls.TAG_FRONTAGE_ROAD),
            ice_road=cls._get_value(d, cls.FIELD_ICE_ROAD, cls.TAG_ICE_ROAD),
            incline=cls._get_value(d, cls.FIELD_INCLINE, cls.TAG_INCLINE),
            junction=cls._get_value(d, cls.FIELD_JUNCTION, cls.TAG_JUNCTION),
            lanes=cls._get_value(d, cls.FIELD_LANES, cls.TAG_LANES),
            lane_markings=cls._get_value(d, cls.FIELD_LANE_MARKINGS, cls.TAG_LANE_MARKINGS),
            lit=cls._get_value(d, cls.FIELD_LIT, cls.TAG_LIT),
            maxspeed=cls._get_value(d, cls.FIELD_MAXSPEED, cls.TAG_MAXSPEED),
            motorroad=cls._get_value(d, cls.FIELD_MOTORROAD, cls.TAG_MOTORROAD),
            mountain_pass=cls._get_value(d, cls.FIELD_MOUNTAIN_PASS, cls.TAG_MOUNTAIN_PASS),
            mtb_scale=cls._get_value(d, cls.FIELD_MTB_SCALE, cls.TAG_MTB_SCALE),
            mtb_scale_uphill=cls._get_value(d, cls.FIELD_MTB_SCALE_UPHILL, cls.TAG_MTB_SCALE_UPHILL),
            mtb_scale_imba=cls._get_value(d, cls.FIELD_MTB_SCALE_IMBA, cls.TAG_MTB_SCALE_IMBA),
            mtb_description=cls._get_value(d, cls.FIELD_MTB_DESCRIPTION, cls.TAG_MTB_DESCRIPTION),
            oneway=cls._get_value(d, cls.FIELD_ONEWAY, cls.TAG_ONEWAY),
            oneway_bicycle=cls._get_value(d, cls.FIELD_ONEWAY_BICYCLE, cls.TAG_ONEWAY_BICYCLE),
            overtaking=cls._get_value(d, cls.FIELD_OVERTAKING, cls.TAG_OVERTAKING),
            parking_lane=cls._get_value(d, cls.FIELD_PARKING_LANE, cls.TAG_PARKING_LANE),
            parking_condition=cls._get_value(d, cls.FIELD_PARKING_CONDITION, cls.TAG_PARKING_CONDITION),
            passing_places=cls._get_value(d, cls.FIELD_PASSING_PLACES, cls.TAG_PASSING_PLACES),
            priority=cls._get_value(d, cls.FIELD_PRIORITY, cls.TAG_PRIORITY),
            priority_road=cls._get_value(d, cls.FIELD_PRIORITY_ROAD, cls.TAG_PRIORITY_ROAD),
            sac_scale=cls._get_value(d, cls.FIELD_SAC_SCALE, cls.TAG_SAC_SCALE),
            service=cls._get_value(d, cls.FIELD_SERVICE, cls.TAG_SERVICE),
            shoulder=cls._get_value(d, cls.FIELD_SHOULDER, cls.TAG_SHOULDER),
            side_road=cls._get_value(d, cls.FIELD_SIDE_ROAD, cls.TAG_SIDE_ROAD),
            smoothness=cls._get_value(d, cls.FIELD_SMOOTHNESS, cls.TAG_SMOOTHNESS),
            surface=cls._get_value(d, cls.FIELD_SURFACE, cls.TAG_SURFACE),
            tactile_paving=cls._get_value(d, cls.FIELD_TACTILE_PAVING, cls.TAG_TACTILE_PAVING),
            tracktype=cls._get_value(d, cls.FIELD_TRACKTYPE, cls.TAG_TRACKTYPE),
            traffic_calming=cls._get_value(d, cls.FIELD_TRAFFIC_CALMING, cls.TAG_TRAFFIC_CALMING),
            trail_visibility=cls._get_value(d, cls.FIELD_TRAIL_VISIBILITY, cls.TAG_TRAIL_VISIBILITY),
            trailblazed=cls._get_value(d, cls.FIELD_TRAILBLAZED, cls.TAG_TRAILBLAZED),
            trailblazed_visibility=cls._get_value(d, cls.FIELD_TRAILBLAZED_VISIBILITY, cls.TAG_TRAILBLAZED_VISIBILITY),
            turn=cls._get_value(d, cls.FIELD_TURN, cls.TAG_TURN),
            width=cls._get_value(d, cls.FIELD_WIDTH, cls.TAG_WIDTH),
            winter_road=cls._get_value(d, cls.FIELD_WINTER_ROAD, cls.TAG_WINTER_ROAD)
        )

    def to_dict(self) -> Dict[str, Any]:
        """Serializes object to a dictionary in the format "attribute:value"."""
        return {
            self.TAG_ABUTTERS: self.abutters,
            self.TAG_BICYCLE_ROAD: self.bicycle_road,
            self.TAG_BUS_BAY: self.bus_bay,
            self.TAG_CHANGE: self.change,
            self.TAG_DESTINATION: self.destination,
            self.TAG_EMBANKMENT: self.embankment,
            self.TAG_EMBEDDED_RAILS: self.embedded_rails,
            self.TAG_FORD: self.ford,
            self.TAG_FRONTAGE_ROAD: self.frontage_road,
            self.TAG_ICE_ROAD: self.ice_road,
            self.TAG_INCLINE: self.incline,
            self.TAG_JUNCTION: self.junction,
            self.TAG_LANES: self.lanes,
            self.TAG_LANE_MARKINGS: self.lane_markings,
            self.TAG_LIT: self.lit,
            self.TAG_MAXSPEED: self.maxspeed,
            self.TAG_MOTORROAD: self.motorroad,
            self.TAG_MOUNTAIN_PASS: self.mountain_pass,
            self.TAG_MTB_SCALE: self.mtb_scale,
            self.TAG_MTB_SCALE_UPHILL: self.mtb_scale_uphill,
            self.TAG_MTB_SCALE_IMBA: self.mtb_scale_imba,
            self.TAG_MTB_DESCRIPTION: self.mtb_description,
            self.TAG_ONEWAY: self.oneway,
            self.TAG_ONEWAY_BICYCLE: self.oneway_bicycle,
            self.TAG_OVERTAKING: self.overtaking,
            self.TAG_PARKING_LANE: self.parking_lane,
            self.TAG_PARKING_CONDITION: self.parking_condition,
            self.TAG_PASSING_PLACES: self.passing_places,
            self.TAG_PRIORITY: self.priority,
            self.TAG_PRIORITY_ROAD: self.priority_road,
            self.TAG_SAC_SCALE: self.sac_scale,
            self.TAG_SERVICE: self.service,
            self.TAG_SHOULDER: self.shoulder,
            self.TAG_SIDE_ROAD: self.side_road,
            self.TAG_SMOOTHNESS: self.smoothness,
            self.TAG_SURFACE: self.surface,
            self.TAG_TACTILE_PAVING: self.tactile_paving,
            self.TAG_TRACKTYPE: self.tracktype,
            self.TAG_TRAFFIC_CALMING: self.traffic_calming,
            self.TAG_TRAIL_VISIBILITY: self.trail_visibility,
            self.TAG_TRAILBLAZED: self.trailblazed,
            self.TAG_TRAILBLAZED_VISIBILITY: self.trailblazed_visibility,
            self.TAG_TURN: self.turn,
            self.TAG_WIDTH: self.width,
            self.TAG_WINTER_ROAD: self.winter_road
        }

    #endregion Serialization
