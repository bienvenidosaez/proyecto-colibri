# coding=utf-8
from tastypie import fields
from tastypie.cache import SimpleCache

from main.api import ColibriResource
from main.fields import OptimizedToOneField
from parliamentarygroup.models import Group, GroupMember, Party


class GroupManagerResource(ColibriResource):
    class Meta:
        queryset = Group.objects.all()
        allowed_methods = ['get']
        filtering = {
            "name": ('exact', 'startswith', 'iexact', 'istartswith',),
            "id": ('exact',),
        }
        resource_name = "simple_group"
        cache = SimpleCache(cache_name='default', timeout=1440)


class GroupResource(GroupManagerResource):
    members = fields.ToManyField(
        'parliamentarygroup.api.GroupMemberResource',
        lambda bundle: bundle.obj.members.through.objects.filter(
            group=bundle.obj.pk).select_related('member') or
        bundle.obj.members, related_name='members_set', full=True)

    class Meta(GroupManagerResource.Meta):
        queryset = Group.objects.all()
        filtering = {
            "name": ('exact', 'startswith', 'iexact', 'istartswith',),
            "id": ('exact',),
        }
        resource_name = "group"


class GroupMemberResource(ColibriResource):
    member = fields.ToOneField(
        'member.api.MemberResource', 'member', full=True)
    party = OptimizedToOneField(
        'parliamentarygroup.api.PartyResource', 'party', null=True)

    class Meta:
        queryset = GroupMember.objects.all().select_related('member')
        allowed_methods = ['get']
        resource_name = "groupmember"
        exclude = ['id']
        include_resource_uri = False
        cache = SimpleCache(cache_name='default', timeout=1440)


class PartyResource(ColibriResource):
    class Meta:
        queryset = Party.objects.all()
        allowed_methods = ['get']
        resource_name = "party"
        filtering = {
            "name": ('exact', 'startswith', 'iexact', 'istartswith',),
            "id": ('exact',),
        }
        cache = SimpleCache(cache_name='default', timeout=1440)
