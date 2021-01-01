import * as React from 'react';
interface IProps {
    year: number;
    value: number;
    onChange: Function;
    defaultValue?: string;
    numeric?: boolean;
    short?: boolean;
    caps?: boolean;
    endYearGiven?: boolean;
    required?: boolean;
    disabled?: boolean;
    id?: string;
    name?: string;
    classes?: string;
    optionClasses?: string;
}
interface IState {
}
export declare class MonthPicker extends React.Component<IProps, IState> {
    renderMonthOptions: () => JSX.Element[];
    handleSelectionChange: (e: any) => any;
    render: () => JSX.Element;
}
export {};
