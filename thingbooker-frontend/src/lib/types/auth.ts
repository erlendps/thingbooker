export type IsAuthenticatedType = {
  isAuthenticated: boolean;
};

export type ShortUserType = {
  id: string;
  username: string;
  avatar: string;
  first_name: string;
};

export type UserType =
  | ShortUserType
  | {
      url: string;
      email: string;
      thingbooker_groups: string[];
      last_name: string;
    };
