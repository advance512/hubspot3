"""
hubspot owners api
"""
from typing import Any, Dict, Optional, Union

from hubspot3.crm_associations import CRMAssociationsClient
from hubspot3.base import BaseClient


OWNERS_API_VERSION = "v3"


class OwnersClient(BaseClient):
    """
    hubspot3 Owners client
    :see: https://developers.hubspot.com/docs/reference/api/crm/owners
    """

    def _get_path(self, subpath: str) -> str:
        """get the full api url for the given subpath on this client"""
        path = f"crm/{OWNERS_API_VERSION}/owners"
        if subpath:
            return f"{path}/{subpath}"
        return path

    def get_owners(
        self,
        limit: int = 100,
        after: Optional[str] = None,
        email: Optional[str] = None,
        archived: bool = False,
        **options: Any,
    ) -> Dict:
        """Get a page of owners."""
        params = {
            "limit": limit,
            "archived": str(archived).lower()
        }
        if after:
            params["after"] = after
        if email:
            params["email"] = email

        response = self._call("", method="GET", params=params, **options)

        return response['results']

    def get_owner_name_by_id(self, owner_id: str, **options: Any) -> str:
        """
        Given an owner's ID, return their full name.
        """
        owner = self.get_owner_by_id(owner_id, **options)
        if owner:
            return f"{owner.get('firstName', '')} {owner.get('lastName', '')}".strip()
        return "value_missing"

    def get_owner_email_by_id(self, owner_id: str, **options: Any) -> str:
        """
        Given an owner's ID, return their email.
        """
        owner = self.get_owner_by_id(owner_id, **options)
        return owner.get("email", "value_missing") if owner else "value_missing"

    def get_owner_by_id(
        self,
        owner_id: str,
        archived: bool = False,
        **options: Any
    ) -> Dict:
        """
        Retrieve an owner by their ID.
        """
        params = {
            "idProperty": "id",
            "archived": str(archived).lower()
        }
        return self._call(str(owner_id), method="GET", params=params, **options)

    def get_owner_by_email(
        self,
        owner_email: str,
        **options: Any
    ) -> Optional[Dict[str, Any]]:
        """
        Retrieve an owner by their email.
        """
        owners = self.get_owners(email=owner_email, **options)
        return owners[0] if owners else None

    def link_owner_to_company(
        self,
        owner_id: Union[str, int],
        company_id: Union[str, int]
    ) -> Dict:
        """
        Link an owner to a company by using their ids.
        """
        associations_client = CRMAssociationsClient(**self.credentials)
        return associations_client.link_owner_to_company(owner_id, company_id)
