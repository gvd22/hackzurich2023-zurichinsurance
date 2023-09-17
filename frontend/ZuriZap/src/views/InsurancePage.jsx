import { useState, useEffect } from "react";
import axios from "axios";
import InsuranceCard from "../components/insurances/InsuranceCard";
import { Spinner } from "@material-tailwind/react";

const InsurancePage = () => {
  const [insurances, setInsurances] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    axios
      .get("https://hackzurich23-backend-emcg5a6iia-oa.a.run.app/insurances")
      .then((response) => {
        setInsurances(response.data);
        setLoading(false);
      })
      .catch((err) => {
        setError(err);
        setLoading(false);
      });
  }, []);

  if (loading) return <Spinner className="h-12 w-12" />;
  if (error) return <div>Error: {error.message}</div>;

  return (
    <div>
      <div className="grid grid-cols-2 gap-3">
        <div className="border p-4 flex flex-col justify-center rounded-lg shadow-md text-white h-[160px] mb-4 bg-cardBg">
          <div>
            <h2 className="inline-block text-2xl">
              Hello, <span className="font-extrabold">Tornike</span>
            </h2>
          </div>
          <p>Check and maintain your insurance status.</p>
        </div>

        <div className="border p-4 flex flex-col justify-center rounded-lg shadow-md text-white h-[160px] mb-4 bg-cardBg">
          <div>
            <h2 className="inline-block text-2xl">
              Total monthly cost:{" "}
              <span className="font-extrabold">$473.90</span>
            </h2>
          </div>
          <p>Next payment: 20 sep. 2023</p>
        </div>
      </div>

      {insurances
        ? insurances.map((insurance) => (
            <InsuranceCard
              key={insurance.id}
              name={insurance.name}
              type={insurance.type}
              price={insurance.price}
            />
          ))
        : "Insurance isn't found"}
    </div>
  );
};

export default InsurancePage;
