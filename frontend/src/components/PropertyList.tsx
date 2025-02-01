import React, { useEffect, useState } from "react";
import Badge from "./Badge";

type PropertyListProps = {
  propertyPath: string;
  propertyPluralName: string;
};

const PropertyList: React.FC<PropertyListProps> = ({ propertyPath, propertyPluralName }) => {
  const [properties, setProperties] = useState<string[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);


  useEffect(() => {
    const fetchProperties = async () => {
      try {
        const response = await fetch(`/api/${propertyPath}`);
        if (!response.ok) {
          throw new Error(`Failed to fetch ${propertyPluralName}`);
        }
        const data = await response.json();
        setProperties(data);
      } catch (err: any) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchProperties();
  }, [propertyPath]);

  if (loading) {
    return <div className="text-center mt-5">Loading...</div>;
  }

  if (error || !properties) {
    return (
      <div className="alert alert-danger text-center mt-5">
        {error ?? `No ${propertyPluralName} found`}
      </div>
    );
  }

  return (
    <div className="container-fluid mt-4">
      <h1 className="mb-4">{propertyPluralName} List ({properties.length})</h1>
      <div className="row d-flex flex-wrap justify-content-start g-3">
        {properties.length > 0 ? (
          <div className="row">
            {properties.map((property, index) => {
              return <Badge key={index} title={property} />;
            })}
          </div>
        ) : (
          <div className="col-12">
            <div className="alert alert-info">
              No {propertyPluralName} found.
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default PropertyList;
