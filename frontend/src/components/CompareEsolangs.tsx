import EsolangDetails from "./EsolangDetails";
import { useEsolangCompare } from "../context/EsolangCompareContext";

const CompareEsolangs: React.FC = () => {
  const { selectedLanguages } = useEsolangCompare();

  return (
    <div className="container-fluid mt-5">
      <h1>Compare Esolangs</h1>
      {selectedLanguages.length < 2 ? (
        <div className="alert alert-warning mt-4">
          Please select two languages to compare
        </div>
      ) : (
        <div className="row">
          {selectedLanguages.map((language) => (
            <div className="col-md-6" key={language}>
              <EsolangDetails name={language} />
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default CompareEsolangs;
